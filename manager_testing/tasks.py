import imutils
import requests
import string
import random

from django.core.files import File
import cv2
from skimage.metrics import structural_similarity as ssim
from celery import Celery
from label_testing.celery import app
from datetime import datetime

# Redis
from manager_testing.models import TestPlan, TestPlanResult, Test
#****************************************************
#celery worker -A label_testing.celery --loglevel=info
#****************************************************


@app.task
def run_tests(test_id):
    print("run_tests")
    test = Test.objects.get(pk=test_id)
    test.is_running = True
    test.running_start_date = datetime.now().astimezone()
    test_plans = TestPlan.objects.all()
    test.total_tests = test_plans.count()
    test.success_test = 0
    test.fail_test = 0
    test.running_end_date = None
    test.save()

    TestPlanResult.objects.filter(test=test).delete()

    cont = 0
    cant = test_plans.count()
    for test_plan in test_plans:
        cont += 1
        #processing_test.delay(test.id, test_plan.id, cont, cant)
        processing_test(test.id, test_plan.id, cont, cant)


def random_string(string_length):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))


def remove_file(file):
    import os
    os.remove(file)
    print("File Removed: ", file)


def add_step(test_plan_result, step, success, result):
    from manager_testing.models import StepResult
    step_result = StepResult()
    step_result.test_plan_result = test_plan_result
    step_result.step = step
    step_result.success = success
    step_result.result = result
    step_result.save()


def add_images(test_plan_result, order, success, image_a, image_b):
    from manager_testing.models import ImageResult
    image_result = ImageResult()
    image_result.test_plan_result = test_plan_result
    image_result.order = order
    image_result.success = success

    if image_a:
        with open(image_a, 'rb') as f:
            contents = File(f)
            image_result.image_a.save(image_a, contents, save=False)
            contents.close()
        f.close()

    if image_b:
        with open(image_b, 'rb') as f:
            contents = File(f)
            image_result.image_b.save(image_b, contents, save=False)
            contents.close()
        f.close()

    image_result.save()


def processing_test(test_id, test_plan_id, cont, cant):
    from manager_testing.models import TestPlanResult
    result = False
    test = Test.objects.get(pk=test_id)
    test_plan = TestPlan.objects.get(pk=test_plan_id)

    test_plan_result = TestPlanResult()
    test_plan_result.test = test
    test_plan_result.test_plan = test_plan
    test_plan_result.result = ""
    test_plan_result.save()
    print("processing test shipment id: ", test_plan.shipment_id)
    step = 0

    try:
        #paso 1
        step = 1
        prod_name_file, test_name_file = download_files(test, test_plan)
        add_step(test_plan_result, step, True, "The files could be downloaded")
        print("step 1: The files could be downloaded")

        #paso 2
        if test_plan.isPdf():
            step = 2
            prod_files_images = convert_pdf_to_image(prod_name_file)
            test_files_images = convert_pdf_to_image(test_name_file)

            remove_file(prod_name_file)
            remove_file(test_name_file)

            if len(prod_files_images) != len(test_files_images):
                print("The number of pages do not match")
                raise Exception("The number of pages do not match")

            has_diff = False
            for i in range(0, len(prod_files_images)):
                prod_file = prod_files_images[i]
                test_file = test_files_images[i]

                # comparo las diferencias
                prod_name_file, test_name_file = diff_image_file(prod_file, test_file)

                if prod_name_file or test_name_file:
                    has_diff = True
                    add_images(test_plan_result, i, False, prod_name_file, test_name_file)
                else:
                    add_images(test_plan_result, i, True, prod_file, test_file)

                remove_file(prod_file)
                remove_file(test_file)

            if has_diff:
                print("There is difference in the pdf")
                raise Exception("There is difference in the pdf")

            add_step(test_plan_result, step, True, "There is no difference in the pdf")
            print("There is no difference in the pdf")
        elif test_plan.isJson():
            step = 2
            prod_zpl_image, test_zpl_image = download_zpl_image_files(test_plan, prod_name_file, test_name_file)

            remove_file(prod_name_file)
            remove_file(test_name_file)

            prod_name_file, test_name_file = diff_image_file(prod_zpl_image, test_zpl_image)

            remove_file(prod_zpl_image)
            remove_file(test_zpl_image)

            has_diff = False
            if prod_name_file or test_name_file:
                add_images(test_plan_result, 0, False, prod_name_file, test_name_file)
                has_diff = True
            else:
                add_images(test_plan_result, 0, True, prod_name_file, test_name_file)

            if has_diff:
                print("There is difference in the images")
                raise Exception("There is difference in the images")
            else:
                add_step(test_plan_result, step, True, "There is no difference in the images")
                print("There is no difference in the images")

        test_plan_result.pass_test = True
        test_plan_result.save()
        result = True

    except Exception as e:
        add_step(test_plan_result, step, False, str(e))
        test_plan_result.pass_test = False
        test_plan_result.save()
        result = False

    if result:
        test.success_test += 1
    else:
        test.fail_test += 1

    if cont == cant:
        test.running_end_date = datetime.now()
        test.is_running = False

    test.save()
    print("finish shipment_id: ", test_plan.shipment_id)


def convert_pdf_to_image(pdf_file):
    from pdf2image import convert_from_path
    pages = convert_from_path(pdf_file, 500)

    files_images = []
    for page in pages:
        path_file = "images/%s.png" % random_string(16)
        page.save(path_file, 'PNG')
        files_images.append(path_file)

    return files_images


def diff_image_file(path_file_prod, path_file_test):
    # load the two input images
    imageA = cv2.imread(path_file_prod)
    imageB = cv2.imread(path_file_test)
    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    (score, diff) = ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")

    if score == 1:
        return None, None

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    path_image_a = "images/%s.png" % random_string(16)
    path_image_b = "images/%s.png" % random_string(16)

    cv2.imwrite(path_image_a, imageA)
    cv2.imwrite(path_image_b, imageB)

    return path_image_a, path_image_b


def download_zpl_image_files(test_plan, path_file_prod, path_file_test):
    url = "http://api.labelary.com/v1/printers/%sdpmm/labels/%sx%s/0/"

    with open(path_file_prod, 'r') as myfile:
        prod_data = myfile.read()

    with open(path_file_test, 'r') as myfile:
        test_data = myfile.read()

    url_json_prod = url % (test_plan.dpmm, test_plan.width, test_plan.height)
    url_json_test = url % (test_plan.dpmm, test_plan.width, test_plan.height)

    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response_prod = requests.post(url_json_prod, data=prod_data, headers=headers)
    response_test = requests.post(url_json_test, data=test_data, headers=headers)

    if response_prod.status_code != 200:
        raise Exception("Error - Downloading prod zpl image file")

    if response_test.status_code != 200:
        raise Exception("Error - Downloading test zpl image file")

    prod_name_file = u"images/%s.png" % random_string(16)
    test_name_file = u"images/%s.png" % random_string(16)

    prod_file = open(prod_name_file, 'w+b')
    prod_file.write(response_test.content)
    prod_file.close()

    test_file = open(test_name_file, 'w+b')
    test_file.write(response_prod.content)
    test_file.close()

    return prod_name_file, test_name_file


def download_files(test, test_plan):
    shipment_id = test_plan.shipment_id
    response_type = test_plan.response_type

    if shipment_id is None:
        return False

    if response_type is None:
        return False

    url_access_point_a = test.get_url_access_point_a()
    url_access_point_b = test.get_url_access_point_b()

    url_access_point_a += "&shipment_ids=%s&response_type=%s" % (shipment_id, response_type)
    url_access_point_b += "&shipment_ids=%s&response_type=%s" % (shipment_id, response_type)

    response_a = requests.get(url_access_point_a)
    if response_a.status_code != 200:
        raise Exception("Error - Downloading access_point A file")

    response_b = requests.get(url_access_point_b)
    if response_b.status_code != 200:
        raise Exception("Error - Downloading access_point B file")

    if test_plan.isPdf():
        name_file_a = u"files/%s.pdf" % random_string(16)
        name_file_b = u"files/%s.pdf" % random_string(16)
    elif test_plan.isZpl():
        name_file_a = u"files/%s.zip" % random_string(16)
        name_file_b = u"files/%s.zip" % random_string(16)
    elif test_plan.isJson():
        name_file_a = u"files/%s.json" % random_string(16)
        name_file_b = u"files/%s.json" % random_string(16)
    else:
        raise Exception("Unsuported response type")

    file_a = open(name_file_a, 'w+b')
    file_a.write(response_a.content)
    file_a.close()

    file_b = open(name_file_b, 'w+b')
    file_b.write(response_b.content)
    file_b.close()

    return name_file_a, name_file_b

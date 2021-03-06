LOGISTIC_TYPES_DS = 'drop_off'
LOGISTIC_TYPES_XD_DS = 'xd_drop_off'
LOGISTIC_TYPES_XD = 'cross_docking'
LOGISTIC_TYPES_FF = 'fulfillment'
LOGISTIC_TYPES_FLEX = 'self_service'

CHOICES_LOGISTIC_TYPES = (
    (LOGISTIC_TYPES_DS, 'Drop off'),
    (LOGISTIC_TYPES_XD_DS, 'Cross docking y Drop off'),
    (LOGISTIC_TYPES_XD, 'Cross docking'),
    (LOGISTIC_TYPES_FF, 'Fulfillment'),
    (LOGISTIC_TYPES_FLEX, 'Flex')
)


SITE_MLB = 'MLB'
SITE_MLA = 'MLA'
SITE_MLC = 'MLC'
SITE_MLU = 'MLU'
SITE_MCO = 'MCO'
SITE_MLM = 'MLM'

CHOICES_SITES = (
    (SITE_MLB, SITE_MLB),
    (SITE_MLA, SITE_MLA),
    (SITE_MLC, SITE_MLC),
    (SITE_MLU, SITE_MLU),
    (SITE_MCO, SITE_MCO),
    (SITE_MLM, SITE_MLM),
)


RESPONSE_TYPE_PDF = 'PDF'
RESPONSE_TYPE_ZPL = 'ZPL2'
RESPONSE_TYPE_JSON = 'JSON'

CHOICES_RESPONSE_TYPE = (
    (RESPONSE_TYPE_PDF, 'PDF'),
    (RESPONSE_TYPE_ZPL, 'ZPL'),
    (RESPONSE_TYPE_JSON, 'JSON'),
)
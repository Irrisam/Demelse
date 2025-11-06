

service_failsafe = [
    ('urgences', 0.0), ('reanimation', 0.0), ('bloc_op', 0.0),
    ('medecine_interne', 0.0), ('biology', 0.0), ('unite_de_soin', 0.0),
    ('ssr', 0.0), ('chirurgie', 0.0), ('endocrino', 0.0),
    ('medecine_specialite', 0.0), ('geriatrie', 0.0),
    ('medecine_generale', 0.0)
]


etab_failsafe = [
    ('hea_cen', 0.0), ('hea_hou', 0.0), ('ssr', 0.0), ('had', 0.0),
    ('home_consult', 0.0), ('teleconsult', 0.0), ('labo', 0.0),
    ('priv_comp', 0.0), ('ehpad_rh', 0.0), ('other_ms', 0.0),
    ('clinic', 0.0), ('hospi', 0.0)
]


rythme_failsafe = [
    ('DAY', 0.0), ('NIGHT', 0.0)
]


def get_failsafes(user_data, data_type=None):
    if user_data.empty:
        if data_type == 'USER_ETAB' or data_type == 'CONTENT_ETAB':
            user_data = etab_failsafe
        if data_type == 'USER_SERVICE' or data_type == 'CONTENT_SERVICE':
            user_data = service_failsafe
        if data_type == 'CONTENT_RYTHME':
            user_data = rythme_failsafe
    return user_data

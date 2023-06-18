# this is where the server settings are for this project
server = '10.10.8.16'
user = 'sandbox'
password = 'Watergate2015'


def get_settings():
    db = 'sw_charts'
    to_return = ('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';UID=' + user + ';PWD=' +
                 password)
    return to_return


def get_sim_soap():
    db = 'sim_soap'
    to_return = ('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';UID=' + user + ';PWD=' +
                 password)
    return to_return


def get_sim_codes():
    db = 'sw_codes'
    to_return = ('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';UID=' + user + ';PWD=' +
                 password)
    return to_return


def get_sim_user():
    db = 'sw_users'
    to_return = ('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';UID=' + user + ';PWD=' +
                 password)
    return to_return


def get_audit():
    db = 'sw_audit'
    to_return = ('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + db + ';UID=' + user + ';PWD=' +
                 password)
    return to_return

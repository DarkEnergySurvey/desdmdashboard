from monitor import pandas_utils


def dashboard_home():

    home_html = '''
        <p>Here we can show the most important dashboard information ..</p>
        <p>Or maybe some information how the dashboard is to be used.</p>
        '''

    sectiondict = {
            'title': 'Dashboard Home',
            'content_html': home_html, 
            }

    return sectiondict


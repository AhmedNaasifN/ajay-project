import logging.handlers

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = '/tmp/updated-sample-app.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

welcome = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <title>Welcome</title>
  <style>
  body {
    color: #333333;
    background-color: #F0F8FF;
    font-family: Arial, sans-serif;
    font-size:14px;
    text-align: center;
  }
  h1 {
    font-size: 300%;
    font-weight: bold;
    color: #0056b3;
    margin-bottom: 20px;
  }
  h2 {
    font-size: 200%;
    font-weight: normal;
    margin-bottom: 20px;
  }
  p {
    font-size: 120%;
    margin: 15px 0;
  }
  a {
    color: #0066cc;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    margin: 10px 0;
  }
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .image {
    margin: 20px 0;
  }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome to Your Updated Python App!</h1>
    <p>This is your newly deployed Python application running in the AWS Cloud.</p>
    <img src="https://via.placeholder.com/400x200" alt="AWS Python App" class="image">
    <h2>Explore the following resources:</h2>
    <ul>
      <li><a href="http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/">AWS Elastic Beanstalk Overview</a></li>
      <li><a href="http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html">Deploy Django Apps to AWS</a></li>
      <li><a href="http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_flask.html">Deploy Flask Apps to AWS</a></li>
      <li><a href="http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.loggingS3.title.html">Working with Logs</a></li>
    </ul>
    <img src="https://via.placeholder.com/400x200" alt="AWS Services" class="image">
  </div>
</body>
</html>
"""

def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            if path == '/':
                request_body_size = int(environ['CONTENT_LENGTH'])
                request_body = environ['wsgi.input'].read(request_body_size)
                logger.info("Received a message: %s", request_body.decode('utf-8'))
            elif path == '/scheduled':
                logger.info("Received task %s scheduled at %s", environ.get('HTTP_X_AWS_SQSD_TASKNAME', 'unknown'),
                            environ.get('HTTP_X_AWS_SQSD_SCHEDULED_AT', 'unknown'))
        except (TypeError, ValueError):
            logger.warning('Error retrieving request body for async work.')
        response = ''
    else:
        response = welcome
    start_response("200 OK", [
        ("Content-Type", "text/html"),
        ("Content-Length", str(len(response)))
    ])
    return [bytes(response, 'utf-8')]

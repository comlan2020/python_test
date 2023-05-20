import socket
import boto3
from botocore.exceptions import ClientError

# specify the list of ports that you want to check on the server
ports = [80, 8080, 8081, 8082,8085]

open_ports=[]
closed_ports=[]


def is_running(host,port):

    """ This function attempts to connect to the given server using a socket.
            Returns: Whether or not it was able to connect to the server. """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return True
    except socket.error:
        return False

# this function is able to check the connection status of each port of the list of ports.
def test_port_server(host):
    for port in ports:
        if is_running(host,port):
            print(f"{host}:{port} is running!")
            open_ports.append(port)
        else:
            print(f'There is a problem with {host}:{port}')
            closed_ports.append(port)

def send_mail():
    """ function to send the check report to the admin """
    # set a verified email address of the admin 
    RECIPIENT = ["<SET A VERIFIED EMAIL OF THE ADMIN>"]
    # set your verified sender email address 
    SENDER = "<SET A VERIFIED EMAIL OF SENDER>"
    SUBJECT = "Check report of ports: {} on the server {} ".format(ports,server)
    if len(open_ports) == 0:
        BODY_TEXT = (f"""
        Hello admin, 
        This mail is to make a quick report of specified ports: {ports} on the server: {server}
        There are no open ports on the server.
        List of closed ports: {closed_ports}
        """)
    elif len(closed_ports) == 0:
        BODY_TEXT = (f"""
        Hello admin, 
        This mail is to make a quick report of specified ports: {ports} on the server: {server}
        List of open ports: {open_ports}
        There are no closed ports on the server.
        """)
    else:
        BODY_TEXT = (f"""
        Hello admin, 
        This mail is to make a quick report of specified ports: {ports} on the server: {server}
        List of open ports: {open_ports}
        List of closed ports: {closed_ports}
        """)           
    CHARSET = "UTF-8"
    # set your aws region <SET YOUR AWS REGION>
    AWS_REGION="<AWS REGION>"
    ses_client = boto3.client('ses', region_name=AWS_REGION)
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")

if __name__== '__main__':
    server=str(input('Enter the address of your server: '))
    test_port_server(server)
    send_mail()
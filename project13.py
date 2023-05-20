import boto3
from botocore.exceptions import ClientError

email=str(input("enter your email address: "))
# set your aws region
AWS_REGION="<AWS_REGION>"
ses_client= boto3.client('ses', region_name=AWS_REGION)
# get a list of verified email for this region
verified_email_list= ses_client.list_verified_email_addresses()
if email in verified_email_list['VerifiedEmailAddresses']:
    # display this message if the email is verified in this region
    print(f"{email} is already verified in this region.")
else:
    print(f"Amazon SES is verifying your email: {email}.")
    # send a verfication mail to the email address an create the identity in AWS SES
    ses_client.verify_email_identity(EmailAddress=email)
    print("check your inbox and click into the link to confirm it")
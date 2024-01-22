# Copy data from an S3 bucket in one account to another w/ Terraform

## Steps
### Everything below is automated in the [GHA here](../../../.github/workflows/copyS3.yaml)
### [Following this guide](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/copy-data-from-an-s3-bucket-to-another-account-and-region-by-using-the-aws-cli.html)
- Ensure both source bucket and destination bucket are created
- apply the Terraform config in this directory
- using the command below, assume the `destination_migration` role defined in [iam.tf](./iam.tf)  
```commandline
 aws sts assume-role \
    --role-arn "arn:aws:iam::<destination_account>:role/<destination_migration_role_name>" \
    --role-session-name AWSCLI-Session
```
- with the following command, verify the role has been successfully assumed
```commandline
aws sts get-caller-identity
```
- copy the data from the source bucket to the destination
```commandline
aws s3 cp s3:// DOC-EXAMPLE-BUCKET-SOURCE / \
    s3:// DOC-EXAMPLE-BUCKET-TARGET / \
    --recursive --source-region us-west-2 --region us-west-2
```
- after data has been copied, run `terraform destroy --auto-approve` and remove the roles and permissions

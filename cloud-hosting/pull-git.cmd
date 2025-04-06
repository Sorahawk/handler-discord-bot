set /p IP=<../../ip.txt
ssh -i ../../ec2.pem ubuntu@%IP% "cd handler-bot && git reset --hard HEAD && git pull"

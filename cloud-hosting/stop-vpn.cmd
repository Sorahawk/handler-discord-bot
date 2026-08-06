set /p IP=<ip.txt
ssh -i ../../ec2.pem ubuntu@%IP% "sudo systemctl stop openvpn-client@surfshark-sg-udp.service"

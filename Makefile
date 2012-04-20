all:	Server	Client	RSA	Bruteforce	Clean

Server:
	python server.py

Client:
	python client.py

RSA:
	python rsa.py

Bruteforce:
	python bruteforce.py

Clean:
	rm *.pyc
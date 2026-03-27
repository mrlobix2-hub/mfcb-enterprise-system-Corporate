MFCB (SMC) Private Limited - Railway / GitHub Deploy Guide

1) ZIP extract karo.
2) GitHub par naya repository banao.
3) Is project ke tamam files repository mein upload karo.
4) Railway account kholo aur GitHub repository connect karo.
5) Railway Variables mein SECRET_KEY set karo.
6) Deploy start ho jayega.
7) DATABASE_URL agar Railway Postgres add karoge to app us ko automatically use karegi.
8) Agar koi fresh deployment ho to seed credentials default mil jayenge:

Director:
Username: MFCB0329
Password: 00447883169211@mfcb

Manager:
Username: manager01
Password: Manager@123

Operator:
Username: operator01
Password: Operator@123

Simple User:
Username: simpleuser01
Password: Client@123

Local Run:
pip install -r requirements.txt
python app.py

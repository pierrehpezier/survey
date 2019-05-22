# survey
Flask python survey

Remove database.db to reset the survey

#dependancies

Ubuntu packages:
```
sudo apt install gunicorn3 -y
```
Python3:
```
pip3 install --user -r requirements.txt
```

# run

```
gunicorn3 --bind 0.0.0.0:8000 server
```


# AfraidDynDNSUpdate
Updates the IPv6 of your device via [Free DNS Afraid.org](https://freedns.afraid.org) so of course you need an account there (which is free) and you need to have already set a [subdomain](https://freedns.afraid.org/subdomain/) to use.

Download and start the script:
```
  python3 afraidUpdate.py
```

On first run it asks for your credentials:
```
  --@server:/testing $ python3 afraidUpdate.py 
  What is the DynDNS url? (something.afraid.org) something.ignorelist.com
  What is your username? YOUR_USERNAME_HERE
  What is your password? YOUR_PASSWORD_HERE
```

Don't worry, your credentials aren't stored in cleartext.

Make it executable and put it in a cronjob to have it run like, idk, like every 30 minutes.

```
  sudo chmod +x afraidUpdate.py 
  sudo crontab -e
  */30 * * * * cd /filePath/to/yourScript && python3 afraidUpdate.py 
```

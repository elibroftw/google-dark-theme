links = ["*://www.google.com", "*://www.google.co.jp", "*://www.google.co.uk", "*://www.google.es", "*://www.google.ca", "*://www.google.de", "*://www.google.it", "*://www.google.fr", "*://www.google.com.au", "*://www.google.com.tw", "*://www.google.nl", "*://www.google.com.br", "*://www.google.com.tr", "*://www.google.be", "*://www.google.com.gr", "*://www.google.co.in", "*://www.google.com.mx", "*://www.google.dk", "*://www.google.com.ar", "*://www.google.ch", "*://www.google.cl", "*://www.google.at", "*://www.google.co.kr", "*://www.google.ie", "*://www.google.com.co", "*://www.google.pl", "*://www.google.pt", "*://www.google.com.pk"]

new_links = []
new_args = []
for link in links:
    for arg in new_args:
        new_links.append(f"{link}/{arg}")
print(str(new_links).replace("'", '"'))

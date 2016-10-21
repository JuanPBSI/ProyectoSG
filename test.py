# Create the body of the message (a plain-text and an HTML version).

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_email(user, pwd, recipient, subject, html, text):
	gmail_user = user
	gmail_pwd = pwd
	From = user
	to = recipient

	msg = MIMEMultipart('alternative')
	msg['Subject'] = subject
	msg['From'] = From
	msg['To'] = to
	#part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')
	#msg.attach(part1)
	msg.attach(part2)
	try:
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.ehlo()
		server.starttls()
		server.login(gmail_user, gmail_pwd)
		server.sendmail(From, to, msg.as_string())
		server.close()
		print 'successfully sent the mail'
	except Exception as cadena:
		print "Error en la conexion SHH: " + format(cadena)

text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
html = """\
<html>
  <head></head>
  <body>
	<style>
		.demo {
			width:100%;
			border:1px dotted #C0C0C0;
			border-collapse:collapse;
			padding:5px;
		}
		.demo caption {
			caption-side:top;
			text-align:center;
		}
		.demo th {
			border:1px dotted #C0C0C0;
			padding:5px;
			background:#006697;
			font-family: verdana;
			color : white;
			font-size: 0.8em;
		}
		.demo td {
			border:1px dotted #C0C0C0;
			text-align:center;
			padding:5px;
			background:#DFE9FF;
		}
	</style>
	<table class="demo">
		<caption>SQLi</caption>
		<thead>
		<tr>
			<th>IP</th>
			<th>Fecha</th>
			<th>Metodo</th>
			<th>Recurso</th>
			<th>Referer</th>
			<th>Codigo<br></th>
			<th>Bytes enviados<br></th>
			<th>Genero error en base de datos<br></th>
			<th>User-Agent</th>
		</tr>
		</thead>
		<tbody>
		<tr>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
			<td>&nbsp;</td>
		</tr>
		</tbody>
	</table>
  </body>
</html>
"""

me = "unam.cert.log.send@gmail.com"
you = "juan_as1991@hotmail.com"
send_email(me, "hola123.,", you, "Hola", html, text)
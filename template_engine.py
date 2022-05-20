
def main_menu_template():
    return '<h1 style="text-align: center;"><title></title><p><strong>Analytics 4.0</strong></p></h1><p>&nbsp;</p><p style="text-align: center;"><a href="/generalized_analysis"><span class="marker">Generalized Analysis</span></a></p><p style="text-align: center;"><a href="/correlation_analysis"><span class="marker">Correlation Analysis</span></a></p>'


def generalized_analysis_template(user_data: list):
    body = '<p>&nbsp;</p><title></title><p>&nbsp;<p style="text-align: center;"><span style="font-size:26px;"><strong>Generalized Analysis</strong></span><span style="font-size:26px;"></span></p></p><form action="/generalized_analysis" method="GET">  <p style="text-align: center;">      User ID:      <input maxlength="4" name="id" type="text" />      <button type="submit" formmethod="get">Search</button>  </p></form><p style="text-align: center;">&nbsp;</p><table style="margin-left: auto; margin-right: auto;" border="1" cellpadding="1" cellspacing="1" height="76" width="499">	<tbody>		<tr>			<td style="text-align: center;">User ID</td>			<td style="text-align: center;">Activity</td>		</tr>'

    # append new lines
    for row in user_data:
        body += f'<tr><td style="text-align: center;">{row[0]}</td><td style="text-align: center;">{row[1]}</td></td>'

    body += '</tbody></table><p>&nbsp;</p>'

    return body


def correlation_template(correlation_coef: float):
    return f'<p style="text-align: center;">&nbsp;</p><title></title><p style="text-align: center;"><span style="font-size:26px;"><strong>Correlation analysis</strong></span></p><p style="text-align: center;"><span style="font-size:14px;"><strong>{correlation_coef}</strong></span></p><p style="text-align: center;"><span style="font-size:14px;"><img alt="" src="http://localhost/correlation_picture" /></span></p>'

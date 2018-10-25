<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><!-- InstanceBegin template="/Templates/pop.dwt.php" codeOutsideHTMLIsLocked="false" -->
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<!-- InstanceBeginEditable name="doctitle" -->
<title>无标题文档</title>
<!-- InstanceEndEditable -->
<!-- InstanceBeginEditable name="head" -->
<!-- InstanceEndEditable -->
<link href="/css/pop.css" rel="stylesheet" type="text/css" />
</head>

<body>
<div id="main">
  <div id="header">
    <p>RNA-Seq Answer </p>
  </div>
  <div id="body"><!-- InstanceBeginEditable name="200" -->
    <div id="text">
      <?php 
		require_once "Smtp.class.php";
		/* 判断输入的是否合理 isset */
		if (empty($_POST["email"]))
		{
			echo "Please input your email!<br />";
		}
		elseif (empty($_POST["data_file"]) and empty($_POST["data_text"]))
		{
			echo "Please input your data!!<br />";
		}
		else/* 输入合理 */
		{
			//******************** email信息 ********************************
			$mailtitle = "RNA-Seq Data Analysis Results";//邮件主题
			$mailcontent= "genome version:".$_POST["genome_version"]."\n"."Estimated time spent is 48 hours";//TXT邮件内容
			//$mailcontent = "<h1>".$mailcontent."</h1>";//HTML邮件内容
			$mailtype = "TXT";//邮件格式（HTML/TXT）,TXT为文本邮件
			//******************** 配置信息 ********************************
			$smtpserver = "smtp.hzau.edu.cn";//SMTP服务器
			$smtpserverport =25;//SMTP服务器端口
			$smtpusermail = "bioaurora@webmail.hzau.edu.cn";//SMTP服务器的用户邮箱
			$smtpemailto = $_POST['email'];//发送给谁
			$smtpuser = "bioaurora@webmail.hzau.edu.cn";//SMTP服务器的用户帐号，注：部分邮箱只需@前面的用户名
			$smtppass = "bioemail3";//SMTP服务器的用户密码(smtp授权码)
			//************************ 配置信息 ****************************
			$smtp = new Smtp($smtpserver,$smtpserverport,true,$smtpuser,$smtppass);//这里面的一个true是表示使用身份验证,否则不使用身份验证.
			$smtp->debug = false;//是否显示发送的调试信息
			$state = $smtp->sendmail($smtpemailto, $smtpusermail, $mailtitle, $mailcontent, $mailtype);
			if($state==""){
				echo "对不起，邮件发送失败！请检查邮箱填写是否有误。";
				echo "<a href='software.html'>点此返回</a>";
				exit();
			}
			else
			{
				echo "恭喜！邮件发送成功！！";
				echo "<a href='software.html'>点此返回</a>";
			}
		}
	?></div>
  <!-- InstanceEndEditable --></div>
  <div id="tail">
    <p>Email ：buzhidao.@gg.com<br />
      huazhong agricultural university Information Institute</p>
  </div>
</div>
</body>
<!-- InstanceEnd --></html>

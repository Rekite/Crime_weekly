<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>범죄가중계_인물검색</title>
</head>
<body>
	<?php
	$db = new mysqli("localhost","celena1004","letme2nplz","celena1004");
	mysqli_set_charset($db,"utf8");
	$name = $_GET["name"];
	$qtest = "select * from tb_name where name='$name'";
	$rtest = mysqli_query($db, $qtest);
	// DB에 해당 인물이 존재하지 않으면 존재하지 않는다고 알림을 준다.
	
	if($rtest->num_rows==0){
		echo "<h1>검색하려는 인물 : ".$name."</h1>";
		echo "<h1> 해당 인물이 존재하지 않습니다.</h1>";
	}

	else{
		$data = $rtest->fetch_row();
		echo "<h1> ".$data[1]." 의 검색 결과입니다.</h1>";
		//이 아래부분 추가해봤는데요
		echo "<table>";
		while($data_row = mysqli_fetch_array($rtest)) 
		{
 			echo '<tr>
 			<td>
 			<img src="'(src링크)'">
 			</td>
 			<td>
 			<a href="melonCrawling.py">' 
 			. $data_row['name'] 
 			. $data_row['group']
 			. $data_row['song']
 			. $data_row['etc']'</a></td></tr>';
		}
	}
		// 해당 인물의 정보를 불러옴
	
	?>

</body>
</html>
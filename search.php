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
	$q = "select * from crime where name='$name'";
	$result = mysqli_query($db, $q);

	// DB에 해당 인물이 존재하지 않으면 존재하지 않는다고 알림을 준다.
	if($result->num_rows==0){
		echo "<h1>검색하려는 인물 : ".$name."</h1>";
		echo "<h1> 해당 인물이 존재하지 않습니다.</h1>";
		}
	// 인물 검색 결과를 table 형식으로 echo한다.
	else{
		$row = $result->fetch_row();
		echo "<h1> ".$row[0]." 의 검색 결과입니다.</h1>";
		echo "<table border='1'>";
		echo '<tr><td rowspan="5">';
		echo '<img src="'. $row[2].'"/></td>';
		echo "<td>데뷔일</td><td>". $row[3]."</td></tr>
		<tr><td>생일</td><td>". $row[4]. "</td></tr>
		<tr><td>타입</td><td>". $row[5]."</td></tr>
		<tr><td>에이전트</td><td>". $row[6]. "</td></tr>
		<tr><td>노래</td><td>". $row[8]. "</td></tr></table>"
		;
	}
	?>

</body>
</html>
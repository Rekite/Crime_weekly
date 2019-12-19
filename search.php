<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>범죄가중계_인물검색</title>
	<link rel="stylesheet" type="text/css" href="CS_css.css">
</head>
<body>

	<?php

	$db = new mysqli("localhost","celena1004","letme2nplz","celena1004");
	mysqli_set_charset($db,"utf8");

	$name = $_GET["name"];
	$q = "select * from crime where name='$name'";
	$result = mysqli_query($db, $q);

	// DB에 해당 인물이 존재하지 않으면 존재하지 않는다고 알림을 준다.
	$person="";
	if($result->num_rows==0){
		echo "<h1>검색하려는 인물 : ".$name."</h1>";
		echo "<h1> 해당 인물이 존재하지 않습니다.</h1>";
		}
	// 인물 검색 결과를 table 형식으로 echo한다.
	else{
		$row = $result->fetch_row();
		echo "<h1> ".$row[0]." 의 검색 결과입니다.</h1>";
		echo "<table class='info'>";
		echo '<tr><td rowspan="5">';echo '<img src="'. $row[2].'" width="300"/></td>';
		echo "<td class='category_tag oddline'>데뷔일</td><td class='result oddline2'>". $row[3]."</td></tr>
		<tr><td class='category_tag evenline'>생일</td><td class='result evenline2'>". $row[4]. "</td></tr>
		<tr><td class='category_tag oddline'>타입</td><td class='result oddline2'>". $row[5]."</td></tr>
		<tr><td class='category_tag evenline'>에이전트</td><td class='result evenline2'>". $row[6]. "</td></tr>
		<tr><td class='category_tag oddline'>노래</td><td class='result oddline2'>". $row[8]. "</td></tr></table>";
		$person = $row[0];
	}
	?>


	<br><input type="button" value="GET NEWS" onclick="searchnews('<?php echo $person;?>');">

	<script type="text/javascript">
		function searchnews(person){
			alert("news crolling is running for"+person);
			//$c_person = person;
			<?php
			//버튼을 클릭하면 python 파일을 실행해 해당 인물의 뉴스를 크롤링한다.
			$output = array();
			exec("python news.py .$c_person, $output");
			echo $output;
			?>

		}
	
	</script>


</body>
</html>
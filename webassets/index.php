<?php
include('includes/top.inc');
?>
<script type="text/javascript">
 function changeImage(element) {
   document.getElementById('imageReplace').src = element; 
 }
</script>

<script type="text/javascript">
 function changeImage2(element) {
   document.getElementById('imageReplace2').src = element; 
 }
</script>
<div id="container">
     <header>Topper </header>
          <section>
		<h2>87.1&deg;F</h2>
	  </section>
     	  <aside>
		<table>
		  <tr>
 		    <td>Humidity:</td><td><strong>30.1 in</strong></td>
		  </tr>
		  <tr>
 		    <td>Pressure:</td><td><strong>30.1 in</strong></td>
		  </tr>
		  <tr>
 		    <td>Rainfall:</td><td><strong>30.1 in</strong></td>
		  </tr>
		  <tr>
 		    <td>Light:</td><td><strong>30.1 in</strong></td>
		  </tr>
		</table>
 </aside>
     <article><h3>Latest Img:</h3></article> 
     <article>
     <h3>Temperature:</h3><span style="display: block; text-align: right">
<a href="#t" onclick="changeImage('wun/Temperature_1h.png');">1h</a>
<a href="#t" onclick="changeImage('wun/Temperature_1d.png');">1d</a>
<a href="#t" onclick="changeImage('wun/Temperature_30d.png');">30d</a>
<a href="#t" onclick="changeImage('wun/Temperature_1y.png');">1y</a></span>
<a name="t"><img src="wun/Temperature_1h.png" alt="Temperature Graph" id="imageReplace"/></a><br />

     <h3>Humidity:</h3><span style="display: block; text-align: right">
<a href="#h" onclick="changeImage2('wun/Humidity_1h.png');">1h</a>
<a href="#h" onclick="changeImage2('wun/Humidity_1d.png');">1d</a>
<a href="#h" onclick="changeImage2('wun/Humidity_30d.png');">30d</a>
<a href="#h" onclick="changeImage2('wun/Humidity_1y.png');">1y</a></span>
<a name="h"><img src="wun/Humidity_1h.png" alt="Humidity Graph" id="imageReplace2"/></a><br />


     </article> 
     <footer>Bottom</footer>
</div>
<?php
include('includes/bottom.inc');
?>

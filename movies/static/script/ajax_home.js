
var domain="http://localhost:8000/"

function search_live()
		{
		var key=document.getElementById('key').value;
		if (event.keyCode == 13) {
        document.getElementById("searchpredict").click();
		return;
    }
		if(event.keyCode>=37 && event.keyCode<=40)
			return
		$.ajax({
			url:domain+'search',
			data:{
			'key':key,
			},
			type:"GET",
			dataType:"json",
			})
			
			.done(function(json)
			{
				if(json["error_flag"])
				{
					openmodal(json["error"]);
					return;
				}
				
				$('#movies').empty();
				result=json['result'];
				for(var i=0;i<result.length;i++)
					{
					console.log(result[i]['name']);
					$('#movies').prepend('<option value="'+result[i]['name']+'-'+ result[i]['year']+ '">');
				}
				
			
			}
			)
		}

/*function predict()
{
	var movie_name=document.getElementById('key').value;
	document.getElementById('searchresult').style.opacity=0.5;
	document.getElementById('logosearch').style.animation='spin 2s linear infinite';
	$.ajax({
			url:domain+'search',
			data:{
			'name':movie_name,
			},
			type:"GET",
			dataType:"json",
			})
			
			.done(function(json)
			{
				if(json["error_flag"])
				{
					alert(json["error"]);
					return;
				}
				document.getElementById('name_predict').innerHTML=json["name"]+"("+json["year"]+")";
				document.getElementById('rating_predict').innerHTML=json["predicted_rating"];
				document.getElementById('verdict').innerHTML=json["verdict"];
				document.getElementById('poster_predict').src=json["poster"];
				document.getElementById('searchresult').style.opacity=0;
				document.getElementById('logosearch').style.animation='';
				
				
				}
				
			
			}
			)
		
}
*/		
function loading_rate()
{
	rate=document.getElementById("ratemidmid");
	rate.style.opacity=0.2;
	rate.style.pointerEvents="none";
	document.getElementById("loader").style.animation="spin 2s linear infinite";
	
	}
function unloading_rate()
{
		rate=document.getElementById("ratemidmid");
		rate.style.opacity=1;
		rate.style.pointerEvents="";
		document.getElementById("loader"    ).style.animation="spin2 2s linear infinite";
	
}
function rate_movie()
		{	
			var movie_id=document.getElementById('movieid').innerHTML;
			console.log(movie_id);
			var rating=0;
			var i=1,cls='';
			var review=document.getElementById("review").value;
			while(i<=5)
			{
				console.log('star'+i)
				console.log(cls)
				cls=document.getElementById('star'+i).className;
				cls=cls.split(' ');
				if(i==1)
				cls=cls[cls.length-1];
				else
				cls=cls[cls.length-2];
				if(cls=='fa-heart-o')
					break;
				rating++;
				i++;
			}
			loading_rate();
			$.ajax({
			url:domain+'rate',
			data:{
			'movieid':movie_id,
			'rating':rating,
			'review':review
			},
			type:"GET",
			dataType:"json",
			
			
			})
			.done(function(json)
			{
			if(json["error_flag"])
				{
					openmodal(json["error"]);
					unloading_rate();
					return;
				}
			
				document.getElementById('movieid').innerHTML=json["movieid"];
				document.getElementById('name').innerHTML=json["name"];
				document.getElementById('year').innerHTML=json["year"];
				document.getElementById('poster').src=json["poster"];
				unloading_rate();
			
			}
			)
			.fail(function( jqXHR, textStatus ) {
			unloading_rate();
				alert( "Request failed: " + textStatus );
			});
			
			}
function skip_movie()
		{
			loading_rate();
			var movie_id=document.getElementById('movieid').innerHTML;
			$.ajax({
			url:domain+'skip',
			data:{
			'movieid':movie_id,
			},
			type:"GET",
			dataType:"json",
			})
			.done(function(json)
			{
				if(json["error_flag"])
				{
					openmodal(json["error"]);
					unloading_rate();
					return;
				}
				
				
				document.getElementById('movieid').innerHTML=json["movieid"];
				document.getElementById('name').innerHTML=json["name"];
				document.getElementById('year').innerHTML=json["year"];
				document.getElementById('poster').src=json["poster"];
				unloading_rate();
			
			}
			)
			.fail(function( jqXHR, textStatus ) {
			unloading_rate();
				alert( "Request failed: " + textStatus );
			});

			
		}
		
		
function a()
		{
		var predict_rating=document.getElementById('rating_predict').getAttribute('content');
		console.log(predict_rating);
		predict_rating=Math.round(predict_rating)
		for(var i=1;i<=5;i++)
		{
			if(i<=predict_rating)
				{
				var star=document.getElementById('star'+i+'_predict');
				var classN="fa fa-3x fa-fw fa-heart";
				var b=star.className.split(' ')
				if(i==1)
					star.className=classN;
				else
					star.className=classN + " " +b[b.length-1];
				console.log(star.className);
				}
				else
				{
				var star=document.getElementById('star'+i+'_predict');
				var classN="fa fa-3x fa-fw fa-heart-o";
				var b=star.className.split(' ')
				if(i==1)
					star.className=classN;
				else
					star.className=classN + " " +b[b.length-1];
				console.log(star.className);
					
					
				}
			
		}
		}
		function stars(v,n,col)
		{
			
			for(var i=1;i<=n;i++)
			{
				document.getElementById('star'+i).className="fa fa-3x fa-fw fa-heart "+col;
			}
			for(var i=n+1;i<=5;i++)
			{
				document.getElementById('star'+i).className="fa fa-3x fa-fw fa-heart-o "+col;
			}
			
		}
		
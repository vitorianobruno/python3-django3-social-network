	function edit(id) {
	
		fetch('/edit/'+ id)
		.then(response => response.json())
		.then(obj => {
			
			//To get all nodes -> element.childNodes;
			// Remove the 'message' DIV element node
			element = document.getElementById('message'+id);
			console.log('REMOVE message');
			element.remove();
			
			var parent = document.getElementById('post'+id);
			
			// Prepare to insert the new DIV 'message'
			var div = document.createElement('div');
			div.setAttribute('id', 'message'+id);
			parent.appendChild(div);
			
			document.querySelector('#message'+id).innerHTML = '<textarea id="text" class="form-control" style="margin-bottom:3px;" name="message" maxlength=500>'+obj['message']+'</textarea> <button class="btn btn-sm btn-outline-primary" id="save" onclick="save('+id+')">Save</button>';		
			
		});
	}
	
	function save(id) {
	
		let text = document.getElementById('text').value;
		console.log(text);
		fetch('/save/'+id, {
		method: 'POST',
		body: JSON.stringify({
			message: text
		})
		})
		.then(response => response.json())
		.then(obj => {
			
			// Remove the 'message' DIV element node
			element = document.getElementById('message'+id);
			console.log('REMOVE message');
			element.remove();
			
			var parent = document.getElementById('post'+id);
			
			// Prepare to insert the new DIV 'message'
			var div = document.createElement('div');
			div.setAttribute('id', 'message'+id);
			parent.appendChild(div);
			
			document.querySelector('#message'+id).innerHTML = '<button id="editMessage" class="btn btn-sm btn-link" onclick="edit('+id+')"/><span>Edit</span></button><br>'+obj['message']+'<br>';	

		});	
	}
	
	function following(id) {
	
		console.log(id);
		
		fetch('/profile_following/'+id, {
		  method: 'PUT',
		  body: JSON.stringify({
		  })
		})

		setTimeout(function(){profile_refresh()}, 700);	
	}
	
	function profile_refresh() {
	
		fetch('/profile_refresh')
		.then(response => response.json())
		.then(obj => {
			
			////////////////////////////////////////////////////////////
			
			// Remove the 'following' DIV element.
			var element = document.getElementById('following');
			console.log('REMOVE following');
			element.remove();
			
			// Remove the 'followers' DIV element.
			element = document.getElementById('followers');
			console.log('REMOVE followers');
			element.remove();
	
			// Get the 'counter' element and ADD DIV's.
			var counter = document.getElementById('counter');
			var div = document.createElement('div');
			div.setAttribute('id', 'following');
			div.style['float'] = 'left';
			div.style['font-size'] = '20px';
			div.style['margin-left'] = '20px';
			counter.appendChild(div);
			
			var div = document.createElement('div');
			div.setAttribute('id', 'followers');
			div.style['float'] = 'left';
			div.style['font-size'] = '20px';
			div.style['margin-left'] = '20px';
			counter.appendChild(div);
			
			var following = document.getElementById('following');
			following.innerHTML = obj['following']+' <span style="font-size:15px;">Following</span>';
			
			var followers = document.getElementById('followers');
			followers.innerHTML = obj['followers']+' <span style="font-size:15px;">Followers</span>';
			
			
			////////////////////////////////////////////////////////////
			
			// Remove the 'users' DIV element
			element = document.getElementById('users');
			console.log('REMOVE users');
			element.remove();
			
			// Prepare to insert the buttons DIV's
			var profile = document.getElementById('profile');
			var div = document.createElement('div');
			div.setAttribute('id', 'users');
			div.style['display'] = 'block';
			div.style['width'] = '100%';
			div.style['height'] = '120px';
			div.style['margin-top'] = '20px';
			div.style['border'] = '1px solid #DCDCDC';
			profile.appendChild(div);
			
			console.log(obj['users'])
			var json = JSON.parse(obj['users']);
			
			for(var user of json){
				
				if (user.pk != obj['request_user_id']){
					
					if (user['fields'].is_active){
						console.log(user)
						var users = document.getElementById('users');
						var div = document.createElement('div');
						div.setAttribute('id', 'button'+user.pk);
						div.style['float'] = 'left';
						div.style['padding'] = '5px 5px 5px 5px';
						div.style['margin-right'] = '10px';
						users.appendChild(div);
						var button = document.getElementById('button'+user.pk);
						button.innerHTML = '<button type="button" class="btn btn-primary btn-sm" onclick="following('+user.pk+')">Unfollow:<b>'+user['fields'].username+'</b></button>';
					}
					else{
						var users = document.getElementById('users');
						var div = document.createElement('div');
						div.setAttribute('id', 'button'+user.pk);
						div.style['float'] = 'left';
						div.style['padding'] = '5px 5px 5px 5px';
						div.style['margin-right'] = '10px';
						users.appendChild(div);
						var button = document.getElementById('button'+user.pk);				
						button.innerHTML = '<button type="button" class="btn btn-secondary btn-sm" onclick="following('+user.pk+')">Follow:<b>'+user['fields'].username+'</b></button>';
					}
					
				}

			}

		});
	}
	
	function like(id) {
	
		console.log(id);
		
		fetch('/like/'+id, {
		  method: 'PUT',
		  body: JSON.stringify({
		  })
		})

		setTimeout(function(){refresh_post(id)}, 700);	
	}
	
	function refresh_post(id) {
	
		fetch('/like_refresh/'+ id)
		.then(response => response.json())
		.then(obj => {
			
			//To get all nodes -> element.childNodes;
			// Remove the 'counter' DIV element node
			element = document.getElementById('counter'+id);
			console.log('REMOVE counter');
			element.remove();
			
			// Get the path#route element node
			var element = document.getElementById('likes'+id);
			var route = element.childNodes[3].childNodes[1].childNodes[1].childNodes[1]; //path#route
			console.log('REMOVE path#route');
			if (typeof route !== "undefined"){
				route.remove();
			}
			
			// Get the #Group element node
			var group = element.childNodes[3].childNodes[1].childNodes[1];
				
			if(obj['like'] == 'False'){
				//console.log('False');
				group.innerHTML = '<path id="route" d="M29.144 20.773c-.063-.13-4.227-8.67-11.44-2.59C7.63 28.795 28.94 43.256 29.143 43.394c.204-.138 21.513-14.6 11.44-25.213-7.214-6.08-11.377 2.46-11.44 2.59z" id="heart" fill="#AAB8C2" />';
			}else{
				group.innerHTML = '<path id="route" d="M29.144 20.773c-.063-.13-4.227-8.67-11.44-2.59C7.63 28.795 28.94 43.256 29.143 43.394c.204-.138 21.513-14.6 11.44-25.213-7.214-6.08-11.377 2.46-11.44 2.59z" id="heart" fill="#E2264D" />';
			}
			
			// Prepare to insert the DIV 'counter'
			var element = document.getElementById('likes'+id);
			var div = document.createElement('div');
			div.setAttribute('id', 'counter'+id);
			div.style['float'] = 'right';
			div.style['fontSize'] = '20px';
			div.style['margin'] = '33px 20px 0 -15px';
			element.appendChild(div);
			document.querySelector('#counter'+id).innerHTML = obj['total'];

		});
	}
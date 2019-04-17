<template lang="pug">
  div#app
    div(
      v-for="item in items"
      :key="item.project_name"
    )
      h1 {{ item.project_name }}
      p {{ item.project_type }}
      button(@click="fetchClaims(item.project_name, 'a-user')") Start labling
    
    br 
    hr 
    br

    div#images
      span(
        v-for="claim in claims"
        :key="claim.id"
      )
        i {{ claim.file_path }}/{{ claim.file_name }} | 
      
    div#image-current
      img
    
    canvas(id="canvas")
</template>


<script>
  export default {
    data: () => ({
      items: [],
      claims: [],
      base64Flag: 'data:image/jpeg;base64,',
      imageb64: '',
      current_claim: 0,
      query: '' 
    }),
    methods: {
      fetchImage(claim_id) {
        var self = this
        fetch('http://localhost:4343/api/image/' + claim_id)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status);
                return;
              }

              response.json().then(function(data) {
                console.log(data.data);
                // self.imageb64 = self.base64Flag + data.data['base64']
                var img = document.querySelector('img');
                img.src = self.base64Flag + data.data['base64'];
                img.style.height = '600px';
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch Error :-S', err);
          });
      },
      fetchClaims(project_name, user_name) {
        var self = this
        fetch('http://localhost:4343/api/claim/project/' + project_name + '/user/' + user_name)
          .then(
            function(response) {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status);
                return;
              }

              response.json().then(function(data) {
                console.log(data.data);
                self.claims = data.data
                self.fetchImage(self.claims[0].id)
                self.current_claim = 0
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch Error :-S', err);
          });
      }
    },
    mounted() {
      var self = this;

      window.addEventListener('keydown', (e)=> {
        var key = e.which || e.keyCode;
        if (key === 39) { // right
          self.current_claim++;
          if (self.current_claim >= self.claims.length) {
            self.current_claim = self.claims.length - 1;
            return;
          }
          self.fetchImage(self.claims[self.current_claim].id);
        }

        else if (key == 37) { //left
          self.current_claim--;
          if (self.current_claim < 0) {
            self.current_claim = 0;
            return;
          }
          self.fetchImage(self.claims[self.current_claim].id);
        }
      });

      fetch('http://localhost:4343/api/projects')
        .then(
          function(response) {
            if (response.status !== 200) {
              console.log('Looks like there was a problem. Status Code: ' +
                response.status);
              return;
            }

            response.json().then(function(data) {
              console.log(data.data);
              self.items = data.data
            });
          }
        )
        .catch(function(err) {
          console.log('Fetch Error :-S', err);
        });
      
      initDraw(document.getElementById('canvas'));

      function initDraw(canvas) {
        function setMousePosition(e) {
            var ev = e || window.event; //Moz || IE
            if (ev.pageX) { //Moz
                mouse.x = ev.pageX + window.pageXOffset;
                mouse.y = ev.pageY + window.pageYOffset;
            } else if (ev.clientX) { //IE
                mouse.x = ev.clientX + document.body.scrollLeft;
                mouse.y = ev.clientY + document.body.scrollTop;
            }
        };

        var mouse = {
            x: 0,
            y: 0,
            startX: 0,
            startY: 0
        };
        var element = null;

        canvas.onmousemove = function (e) {
            setMousePosition(e);
            if (element !== null) {
                element.style.width = Math.abs(mouse.x - mouse.startX) + 'px';
                element.style.height = Math.abs(mouse.y - mouse.startY) + 'px';
                element.style.left = (mouse.x - mouse.startX < 0) ? mouse.x + 'px' : mouse.startX + 'px';
                element.style.top = (mouse.y - mouse.startY < 0) ? mouse.y + 'px' : mouse.startY + 'px';
            }
        }

        canvas.onclick = function (e) {
            if (element !== null) {
                console.log('width: ' + element.style.width + ', height: ' + element.style.height);
                element = null;
                canvas.style.cursor = "default";
                console.log("finsihed.");
            } else {
                console.log("begun.");
                mouse.startX = mouse.x;
                mouse.startY = mouse.y;
                element = document.createElement('div');
                element.className = 'rectangle'
                element.style.left = mouse.x + 'px';
                element.style.top = mouse.y + 'px';
                element.style.border = '1px solid #FF0000';
                element.style.display = 'absolute';
                canvas.appendChild(element)
                canvas.style.cursor = "crosshair";
            }
        }
      }
    }
  }
</script>

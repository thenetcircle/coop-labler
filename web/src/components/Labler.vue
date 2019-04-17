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
      div(
        v-for="claim in claims"
        :key="claim.id"
      )
        p {{ claim.file_path }}/{{ claim.file_name }}
</template>

<script>
  export default {
    data: () => ({
      items: [],
      claims: [],
      query: '' 
    }),
    methods: {
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
              });
            }
          )
          .catch(function(err) {
            console.log('Fetch Error :-S', err);
          });
      }
    },
    mounted() {
      var self = this
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
    }
  }
</script>

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
      
    canvas(v-canvas)
</template>

<script>
  import { v4 } from 'uuid'

  export default {
    data: () => ({
      items: [],
      claims: [],
      base64Flag: 'data:image/jpeg;base64,',
      imageb64: '',
      current_claim: 0,
      query: '',

      // register the custom directive
      directives: {
        canvas,
      },
    }),

    methods: {
      fetchImage(claimId) {
        const self = this

        fetch('http://localhost:4343/api/image/' + claimId)
          .then((response) => {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status)
                return
              }

              response.json().then((data) => {
                const base64Key = 'base64'
                const img = document.querySelector('img')
                img.src = self.base64Flag + data.data[base64Key]
                img.style.height = '600px'
              })
            },
          )
          .catch((err) => {
            console.log('Fetch Error :-S', err)
          })
      },

      fetchClaims(projectName, userName) {
        const self = this

        fetch('http://localhost:4343/api/claim/project/' + projectName + '/user/' + userName)
          .then((response) => {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status)
                return
              }

              response.json().then((data) => {
                console.log(data.data)
                self.claims = data.data
                self.fetchImage(self.claims[0].id)
                self.current_claim = 0
              })
            },
          )
          .catch((err) => {
            console.log('Fetch Error :-S', err)
          })
      },
    },
    mounted() {
      const self = this

      window.addEventListener('keydown', (e) => {
        const key = e.which || e.keyCode

        if (key === 39) { // right
          self.current_claim++
          if (self.current_claim >= self.claims.length) {
            self.current_claim = self.claims.length - 1
            return
          }
          self.fetchImage(self.claims[self.current_claim].id)
        }
        else if (key === 37) { // left
          self.current_claim--
          if (self.current_claim < 0) {
            self.current_claim = 0
            return
          }
          self.fetchImage(self.claims[self.current_claim].id)
        }
      })

      fetch('http://localhost:4343/api/projects')
        .then((response) => {
            if (response.status !== 200) {
              console.log('Looks like there was a problem. Status Code: ' +
                response.status)
              return
            }

            response.json().then((data) => {
              console.log(data.data)
              self.items = data.data
            })
          },
        )
        .catch((err) => {
          console.log('Fetch Error :-S', err)
        })
    },
  }
</script>

<style>
canvas {
  background: navy;
}
</style>

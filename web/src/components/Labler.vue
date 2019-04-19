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
      
    canvas#labler(v-foobar)
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
    }),

    // register the custom directive
    directives: {
      foobar: {
        inserted(el) {
          const canvas = el
          const ctx = canvas.getContext('2d')

          if (ctx === null) {
            return
          }

          canvas.width = 1000
          canvas.height = 800

          ctx.lineJoin = 'round'
          ctx.lineCap = 'round'
          ctx.lineWidth = 5

          let prevPos = {
            offsetX: 0,
            offsetY: 0,
          }

          let line = []
          let isPainting = false
          const userId = v4()
          const USER_STROKE = 'red'

          function handleMouseDown(e) {
            const {
              offsetX,
              offsetY,
            } = e
            prevPos = {
              offsetX,
              offsetY,
            }
            isPainting = true
          }

          function endPaintEvent() {
            if (isPainting) {
              isPainting = false
              sendPaintData()
            }
          }

          function handleMouseMove(e) {
            if (isPainting) {
              const {
                offsetX,
                offsetY,
              } = e

              const offSetData = {
                offsetX,
                offsetY,
              }

              const positionInfo = {
                start: {
                  ...prevPos,
                },
                stop: {
                  ...offSetData,
                },
              }
              line = line.concat(positionInfo)
              paint(prevPos, offSetData, USER_STROKE)
            }
          }

          function sendPaintData() {
            const body = {
              line,
              userId,
            }
            fetch('http://localhost:4000/paint', {
              method: 'post',
              body: JSON.stringify(body),
              headers: {
                'content-type': 'application/json',
              },
            }).then(() => (line = []))
          }

          function paint(prevPosition, currPosition, strokeStyle) {
            const {
              offsetX,
              offsetY,
            } = currPosition

            const {
              offsetX: x,
              offsetY: y,
            } = prevPosition

            if (ctx === null) {
              return
            }

            ctx.beginPath()
            ctx.strokeStyle = strokeStyle
            ctx.moveTo(x, y)
            ctx.lineTo(offsetX, offsetY)
            ctx.stroke()

            prevPos = {
              offsetX,
              offsetY,
            }
          }

          canvas.addEventListener('mousedown', handleMouseDown)
          canvas.addEventListener('mousemove', handleMouseMove)
          canvas.addEventListener('mouseup', endPaintEvent)
          canvas.addEventListener('mouseleave', endPaintEvent)
        },
      },
    },

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
                const heightKey = 'height'
                const widthKey = 'width'
                const img = document.querySelector('img')
                const labler = document.getElementById('labler')
                const width = data.data[widthKey]
                const height = data.data[heightKey]
                const resizeRatio = 600 / height

                img.src = self.base64Flag + data.data[base64Key]
                img.style.height = '600px'
                
                const rect = img.getBoundingClientRect();
                console.log(rect.top, rect.right, rect.bottom, rect.left);

                labler.height = 600
                labler.width = width * resizeRatio
                labler.style.position = "absolute";
                labler.style.left = rect.left + 'px'

                // TODO: for some reason the image shifts 64px up after checking where it is
                labler.style.top = (rect.top - 64) + 'px'
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
canvas#labler {
  background: rgba(0,0,255,0.5);;
  position: absolute;
  top: 2000;
  left: 0;
}
</style>

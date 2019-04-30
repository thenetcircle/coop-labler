<template lang="pug">
  div#app
    div(
      v-for="item in items"
      :key="item.project_name"
    )
      h1 Project: {{ item.project_name }}
      p Project Type: {{ item.project_type }}
      a(@click="fetchClaims(item.project_name, userName)") Start labling
    
    br 
    hr 
    br

    span#arrow-help 
      b User the arrow keys to change image.
      
    div
      div#image-current(width='50%', style='float: left;')
        img
      
      div#image-labels(width='50%', style='float: left;')
        b Labels for image
        div#labels
          i asdf
      
    canvas#labler(v-labler)
</template>

<script>
  export default {
    data: () => ({
      items: [],
      claims: [],
      base64Flag: 'data:image/jpeg;base64,',
      imageb64: '',
      currentClaim: 0,
      currentClaimId: 0,
      query: '',
      userId: 1234,
      userName: 'a-user',
    }),

    // register the custom directive
    directives: {
      labler: {
        inserted(el, binding, vnode) {
          const self = this
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

          let startPos = {
            offsetX: 0,
            offsetY: 0,
          }
          let offsetPos = {
            offsetX: 0,
            offsetY: 0,
          }

          let line = []
          let isPainting = false
          const USER_STROKE = 'red'

          function handleMouseDown(e) {
            const {
              offsetX,
              offsetY,
            } = e
            const {
              startX,
              startY,
            } = e
            startPos = {
              offsetX,
              offsetY,
            }
            isPainting = true
          }

          // TODO: should be able to draw multiple rectangles
          // on a single image, and they should load agin when
          // going back to a previous image
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

              offsetPos = {
                offsetX,
                offsetY,
              }

              paint(offsetPos, USER_STROKE)
            }
          }

          function sendPaintData() {
            const vself = vnode.context
            const userId = vnode.context.userId

            const body = {
              // list of labels, each can have different target_class
              labels: [{
                xmin: Math.floor(startPos.offsetX / vself.resizeRatio),
                ymin: Math.floor(startPos.offsetY / vself.resizeRatio),
                xmax: Math.floor(offsetPos.offsetX / vself.resizeRatio),
                ymax: Math.floor(offsetPos.offsetY / vself.resizeRatio),
                target_class: 0,
              }],
              resize: vself.resizeRatio,
              project_type: 'localization',
              user_id: vself.userId,
            }
            console.log(body)

            // TODO: only submit when changing picture, IF any labels have changed
            fetch('http://localhost:4343/api/v1/submit/' + vself.currentClaimId, {
              method: 'post',
              body: JSON.stringify(body),
              headers: {
                'content-type': 'application/json',
              },
            }).then(() => (line = []))
          }

          function paint(currPosition, strokeStyle) {
            const {
              offsetX,
              offsetY,
            } = currPosition

            const {
              offsetX: x,
              offsetY: y,
            } = startPos

            if (ctx === null) {
              return
            }

            // beginPath is needed, otherwise the previous rectangles won't be cleared
            ctx.beginPath()

            // store the current transformation matrix
            ctx.save()

            // use the identity matrix while clearing the canvas
            ctx.setTransform(1, 0, 0, 1, 0, 0)
            ctx.clearRect(0, 0, canvas.width, canvas.height)

            // restore the transform
            ctx.restore()

            // draw our current rectable from origin to current mouse position
            ctx.rect(x, y, offsetX - x, offsetY - y)
            ctx.strokeStyle = strokeStyle
            ctx.stroke()
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

        fetch('http://localhost:4343/api/v1/image/' + claimId)
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
                const labelsKey = 'labels'
                const img = document.querySelector('img')
                const labler = document.getElementById('labler')
                const width = data.data[widthKey]
                const height = data.data[heightKey]
                const imgLabels = data.data[labelsKey]
                self.resizeRatio = 600 / height

                img.src = self.base64Flag + data.data[base64Key]
                img.style.height = '600px'

                const rect = img.getBoundingClientRect()
                console.log(rect.top, rect.right, rect.bottom, rect.left)

                labler.height = 600
                labler.width = width * self.resizeRatio
                labler.style.position = 'absolute'
                labler.style.left = rect.left + 'px'

                // TODO: for some reason the image shifts 64px up after checking where it is
                labler.style.top = (rect.top - 64) + 'px'

                const labels = document.getElementById('labels')
                while (labels.firstChild) {
                    labels.removeChild(labels.firstChild);
                }

                console.log(data)
                for (var i = 0; i < imgLabels.length; i++) {
                  const labelSpan = document.createElement('span');
                  var text = document.createTextNode(imgLabels[i].xmin + '<br />');
                  labelSpan.appendChild(text);
                  labels.appendChild(labelSpan);
                }
              })
            },
          )
          .catch((err) => {
            console.log('Fetch Error :-S', err)
          })
      },

      fetchClaims(projectName, userName) {
        const self = this

        fetch('http://localhost:4343/api/v1/claim/project/' + projectName + '/user/' + userName)
          .then((response) => {
              if (response.status !== 200) {
                console.log('Looks like there was a problem. Status Code: ' +
                  response.status)
                return
              }

              response.json().then((data) => {
                console.log(data.data)

                self.claims = data.data
                self.currentClaimId = self.claims[0].id
                self.currentClaim = -1
                document.getElementById('arrow-help').style.display = 'block'

                // TODO: if we set currentClaim to 0 and fetch it here, the
                // x/y submitted will be wrong for some reason. Instead, for
                // now, force the user to use the arrow keys to begin... Turns
                // out the coordinates will be correct because of this.
                // self.fetchImage(self.currentClaimId)
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
          self.currentClaim++
          if (self.currentClaim >= self.claims.length) {
            self.currentClaim = self.claims.length - 1
            return
          }
          self.fetchImage(self.claims[self.currentClaim].id)
        }
        else if (key === 37) { // left
          self.currentClaim--
          if (self.currentClaim < 0) {
            self.currentClaim = 0
            return
          }
          self.fetchImage(self.claims[self.currentClaim].id)
        }
      })

      fetch('http://localhost:4343/api/v1/projects')
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
div#app {
  padding-left: 25px;
  padding-top: 25px;
}

canvas#labler {
  background: rgba(0,0,255,0.0);
  position: absolute;
  top: 2000;
  left: 0;
}

span#arrow-help {
  display: none;
}
</style>

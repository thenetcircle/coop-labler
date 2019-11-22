## List projects

Request:

`curl localhost:4343/api/v1/projects`

Response:

```json
{
	"data": [{
		"classes": 3,
		"created": "2019-04-16T07:46:22Z",
		"directory": "/data/dw/images/2019",
		"finished": "",
		"id": 1,
		"project_name": "some-project-name",
		"project_type": "localization"
	}],
	"message": "",
	"status_code": 200
}
```

## Claim examples to label

Calling this endpoint will return up to 10 claims. Calling this api twice without 
labeling any of the claims will return the same 10 claims. If a user labels e.g. 2
of these claims, then call this api again, the remaining 8 claims plus 2 new claims
will be returned (if there are any remaining unclaimed examples).

Request:

<code>curl localhost:4343/api/v1/claim/project/some-project-name/user/<b><i>a-user</i></b></code>

Response:

```json
{
	"data": [{
		"claimed_at": "2019-04-30T01:49:25Z",
		"claimed_by": "a-user",
		"file_name": "10033.jpg",
		"file_path": "/data/dw/images/2019",
		"id": 21,
		"project_name": "some-project-name",
		"status": "waiting"
	}, {
	// [...]
	}, {
		"claimed_at": "2019-04-17T07:38:04Z",
		"claimed_by": "a-user",
		"file_name": "cars.jpg",
		"file_path": "/tmp",
		"id": 9,
		"project_name": "some-project-name",
		"status": "waiting"
	}],
	"message": "",
	"status_code": 200
}
```

## Get image for claim

The image data is returned in base64 encoding.

Request:

<code>curl localhost:4343/api/v1/image/<b><i>claim_id</i></b></code>

Response:

```json
{
	"data": {
		"base64": "/9j/4AAQSkZJ[...]w2H7vFFFMR/9k=",
		"height": 500,
		"width": 960
	},
	"message": "",
	"status_code": 200
}
```

## Submit labels for a claim

Data:

```json
{
	"project_type": "localization",
	"labels": [{
		"xmin": 12,
		"xmax": 90,
		"ymin": 210,
		"ymax": 280,
		"target_class": "dog"
	}]
}
```

Request:

```bash
curl -X POST \
    -H 'Content-Type: application/json' \
	localhost:4343/api/v1/submit/<claim_id> \
	-d @data.json
```

Or: 

```bash
curl -X POST \
    -H 'Content-Type: application/json' \
	localhost:4343/api/v1/submit/<claim_id> \
	-d '{"project_type":"localization","labels":[{"xmin":12,"xmax":90,"ymin":210,"ymax":280,"target_class":"dog"}]}'
```

Response:

```json
{
	"data": {},
	"message": "",
	"status_code": 200
}
```

## Unique labels for project

Returns a list of unique labels for a project.

Request:

`curl localhost:4343/api/v1/labels/project/some-project-name`

Response:

```json
{
    "data": [
        "cat",
        "dog"
    ],
    "message":"",
    "status_code":200
}
```

## Project overview

Overview returns a list of labeled examples and a list of unlabeled examples. Each image is a 500x500 px 
thumbnail, where the label coordinates are positions on the full sized image, not the thumbnail.

Request:

`curl localhost:4343/api/v1/overview/project/some-project-name`

Response:

```json
{
	"data": {
		"done": [{
			"base64": "/9j/4SkZJ[...]NFWLP/9k=",
			"height": 500,
			"width": 500,
			"labels": [{
				"id": 10,
				"status": "finished",
				"target_class": "dog",
				"xmax": 592,
				"xmin": 399,
				"ymax": 538,
				"ymin": 263
			}, 
			// [...]
			{
				"id": 11,
				"status": "finished",
				"target_class": "cat",
				"xmax": 791,
				"xmin": 625,
				"ymax": 520,
				"ymin": 262
			}]
		}],
		"remaining": [{
			"base64": "/9j/4AA[...]P/9k=",
			"height": 500,
			"width": 500,
			"labels": []
		}]
	},
	"message": "",
	"status_code": 200
}
```

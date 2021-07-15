## effects controller

One effect at a time, uses rep-req with zmq for image transfer. In the future
this can be extended to push pull or pub-sub when multiple services have to be
chained or multipe instances of the same service can be instantiated to do
multi batch inference using mutliple processes of the effects service.


Each of the effects can be enabled by implementing the postprocess function in 
`Effect` class in `./server/src/effects_container/effects/effects.py`, 
object detection effect has be imepemented, here `./server/src/effects_container/effects/obj_detect.py`
defining the postprocessing function. Also, the path of the model is given and optional
details needed for any preprocessing.


Each effect uses at its core Tensorflow model hub to load the model from the model
path given by the implementor. Once the model infers the results. The results and
image is given to the `postprocessing` method. Each effect will have its own setup
and code. Each of the effect can be added to `./server/src/effects_container/effects`
directory.


### Architecture of effects conainer service interaction with AI server

```bash
               push-pull / pub-sub (future)
  ┌─────────────────────────────────┐
  │                                 │
  │                                 │
  │                  chained effects│
  │                                 │
  │           ┌────┐    ┌───┐    ┌──┴┐
  │  rep/req  │    │    │   │    │   │
  │   ┌──────►│ e1 ├───►│ e2├───►│e3 │
  │   │       └────┘    └───┘    └───┘
  ▼   ▼
┌───────┐     ┌────┐
│  ai   ├────►│    │      effects
│server │     │ e2 │      server
└──────┬┘     └────┘
       │
       │      ┌────┐
       │      │    │
       └─────►│ e1 │
      rep/req └────┘


              multi instance
              of effects pipeline
```

### Client

Effects client to test the server

### Server

Effect conainer server that features object detecton from tfhub as the effect


# PIX 2 PIX

### Background


### Instructions

#### Set up
1. If you have not done so already, clone the usecases repo into your local workspace
```bash
git clone https://github.com/intel/stacks-usecase
```
```bash
cd usecases/tensorflow/pix2pix
```
2. Run the Deep Learning Reference Stack (DLRS)
```bash
docker run -it -v ${PWD}:/workdir clearlinux/stacks-dlrs-mkl
```
3. Navigate to the github usecase and install requirements
```bash
cd /workdir
```
```bash
pip install -r requirements.txt
```
4. Download the data and process it
```bash
python scripts/get_data.py
```
```bash
python scripts/split.py
```

#### Training
Run training
```bash
python main.py
```

If you want to adjust hyperparamaters like cycles, epochs, and batche_size, or even train the discriminator or generator separately, add them as arguments. For example:
```bash
python main.py --model continue --epochs 5 --batch_size 12 --cycles 5
```

Available options are:
* model (string)
    * continue - run models named 'generator_model.h5' and 'discriminator_model.h5' in the 'models' directory
    * checkpoint - run the latest model in the 'checkpoints' directory
* epochs (int)
* batch_size (int)
* cycles (int)

#### Inference
```bash
python infer.py
```


### Testing

- Move to pix2pix directory 
- Install test requirements using:

```bash
pip install -r test-requirements.txt
```

- Run 

```bash
python -m pytest
```

## Citation
```
@article{pix2pix2017,
  title={Image-to-Image Translation with Conditional Adversarial Networks},
  author={Isola, Phillip and Zhu, Jun-Yan and Zhou, Tinghui and Efros, Alexei A},
  journal={CVPR},
  year={2017}
}
```
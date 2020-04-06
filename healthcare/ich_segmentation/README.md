## intracranial hemorrhage detection

To run training locally:

1. Extract compressed data from [physionet](https://physionet.org/content/ct-ich/1.3.1/) into the ICH-UNET-2020 directory
2. Run main.py with the '--local' flag
```bash
python main.py --local
```
3. The model will be saved as a checkpoint in 'models/checkpoints/' and it will write or overwrite 'models/unet.h5'


To run inference locally:

1. Extract compressed data from [physionet](https://physionet.org/content/ct-ich/1.3.1/) into the ICH-UNET-2020 directory
2. Run main.py with the '--infer' flag

    Note: There must be a model saved in 'models/checkpoints/' named 'unet.h5'
```bash
python main.py --infer
```


There are additional options and flags. For a full list, run
```bash
python main.py --help
```


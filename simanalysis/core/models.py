import h5py
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

from simanalysis.utils import listdir_absolute


class H5FileGroup:

    def __init__(self, _dir: str):

        self.directory = _dir
        self.paths = listdir_absolute(self.directory)
        self.filenames = [os.path.basename(path) for path in self.paths]

    def __repr__(self):

        _repr = f"Directory:\r\r{self.directory}\r"

        _repr += "Files included in group:\r\r"
        for i, p in enumerate(self.paths):
            if i == 30:
                _repr += "\t- -------------\n\n"
            elif 30 < i < len(self.paths):
                pass
            elif i == len(self.paths):
                _repr += f"\t- {p}\n"
            else:
                _repr += f"\t- {p}\n"

        return _repr

    def print_dtype(self, v):

        for path in self.paths:

            file = h5py.File(path, 'r')
            print(file[v].dtype.names)

    def plot_charge(self, filename: str):

        charge = np.asarray([])
        zenith = np.asarray([])

        for path in tqdm(self.paths):

            file = h5py.File(path, 'r')

            # Check and concatenate datasets if they exist
            if 'Homogenized_QTot' in file and "PolyplopiaPrimary" in file:
                zenith = np.concatenate((zenith, file['PolyplopiaPrimary']['zenith'][:]))
                charge = np.concatenate((charge, file['Homogenized_QTot']['value'][:]))

            file.close()

        # Plot the histograms
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)
        log_charge_bins = np.linspace(1, 5, 50)
        ax.hist(np.log10(charge), bins=log_charge_bins, alpha=0.5)
        ax.set_ylabel('Number of Events')
        ax.set_xlabel(r'log$_{10}$(charge)')
        ax.set_yscale('log')

        cos_zenith_bins = np.linspace(-1, 1, 20)
        ax2.hist(np.cos(zenith), bins=cos_zenith_bins, alpha=0.5)
        ax2.set_ylabel('Number of Events')
        ax2.set_xlabel(r'cos($\theta$)')

        plt.tight_layout()
        fig.savefig(filename, dpi=300)


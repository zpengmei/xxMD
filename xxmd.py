import os
import os.path as osp
import ase
import ase.io
import torch

from torch_geometric.data import (
    Data,
    InMemoryDataset,
    download_url,
    extract_tar,
    extract_zip,
)


class xxMD(InMemoryDataset):

    xxMD_url = 'https://raw.githubusercontent.com/zpengmei/xxMD/main'

    file_names = {
        'azo_dft': 'xxMD-DFT/azo/azo.zip',
        'dia_dft': 'xxMD-DFT/dia/dia.zip',
        'mal_dft': 'xxMD-DFT/mal/mal.zip',
        'sti_dft': 'xxMD-DFT/sti/sti.zip',
        'azo_cas_s0': 'xxMD-CASSCF/azo/s0/azo_s0.zip',
        'azo_cas_s1': 'xxMD-CASSCF/azo/s1/azo_s1.zip',
        'azo_cas_s2': 'xxMD-CASSCF/azo/s2/azo_s2.zip',
        'dia_cas_s0': 'xxMD-CASSCF/dia/s0/dia_s0.zip',
        'dia_cas_s1': 'xxMD-CASSCF/dia/s1/dia_s1.zip',
        'dia_cas_s2': 'xxMD-CASSCF/dia/s2/dia_s2.zip',
        'mal_cas_s0': 'xxMD-CASSCF/mal/s0/mal_s0.zip',
        'mal_cas_s1': 'xxMD-CASSCF/mal/s1/mal_s1.zip',
        'mal_cas_s2': 'xxMD-CASSCF/mal/s2/mal_s2.zip',
        'sti_cas_s0': 'xxMD-CASSCF/sti/s0/sti_s0.zip',
        'sti_cas_s1': 'xxMD-CASSCF/sti/s1/sti_s1.zip',
        'sti_cas_s2': 'xxMD-CASSCF/sti/s2/sti_s2.zip',
    }

    def __init__(self, root, name, split, transform=None, pre_transform=None, pre_filter=None):
        self.name = name
        self.split = split
        processed_path = osp.join(root, name, 'processed', f'data_{split}.pt')
        if not osp.exists(processed_path):
            super(xxMD, self).__init__(root, transform, pre_transform, pre_filter)
            self.process()
        self.data, self.slices = torch.load(processed_path)



    def mean(self) -> float:
        return float(self._data.energy.mean())

    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, self.name, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, self.name, 'processed')

    @property
    def raw_file_names(self) -> str:
        name = self.file_names[self.name]
        return name

    @property
    def processed_file_names(self):
        return [f'data_{self.split}.pt']

    def download(self):
        url = f'{self.xxMD_url}/{self.file_names[self.name]}'
        path = download_url(url, self.raw_dir)
        print(path)
        extract_zip(path, self.raw_dir)
        os.unlink(path)

    def process(self):
        # Get list of all files in raw_dir
        all_files = os.listdir(self.raw_dir)
        
        # Filter files based on self.split
        split_files = [f for f in all_files if self.split in f]

            # Process each file
        for file in split_files:
            raw_path = osp.join(self.raw_dir, file)
            processed_path = osp.join(self.processed_dir, f'data_{self.split}.pt')
            
            # Read and process raw data
            frames = ase.io.read(raw_path, index=':', format='extxyz')

            data_list = []
            for i in range(len(frames)):
                frame = frames[i]
                z = torch.from_numpy(frame.numbers).long()
                pos = torch.from_numpy(frame.positions).float()
                energy = torch.tensor(frame.get_potential_energy()).float()
                forces = torch.from_numpy(frame.get_forces()).float()
                data = Data(z=z, pos=pos, energy=energy, force=forces, ase_frame=frame)
                if self.pre_filter is not None and not self.pre_filter(data):
                    continue
                if self.pre_transform is not None:
                    data = self.pre_transform(data)
                data_list.append(data)
            
            # Save processed data
            torch.save(self.collate(data_list), processed_path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self)}, name='{self.name}')"
import os
import numpy as np
import struct
import open3d as o3d

class bin_pcd_converter():
    """
    Class to convert a .bin to a .pcd file and vice versa. 
    """
    def __init__(self, input_file, output_folder):
        self.input_file = input_file
        self.output_folder = output_folder
        self.size_float = 4
        self.list_pcd = []
        self.list_intensity = []
        self.basename, self.input_format = os.path.splitext(os.path.basename(self.input_file))
        if self.input_format == ".bin":
            self.output_file = os.path.join(self.output_folder, self.basename + ".pcd")
        elif self.input_format == ".pcd":
            self.output_file = os.path.join(self.output_folder, self.basename + ".bin")
        else:
            raise "Input file should be a .bin or .pcd file."
        
        self.convert()

    def read_bin(self):
        """Method to read a point cloud from a .bin file"""
        with open (self.input_file, "rb") as f:
            byte = f.read(self.size_float*4)
            while byte:
                x,y,z,intensity = struct.unpack("ffff", byte)
                self.list_pcd.append([x, y, z])
                self.list_intensity.append(intensity)
                byte = f.read(self.size_float*4)
                
    def read_pcd(self):
        """Method to read a point cloud from a .pcd file"""
        pcd = o3d.io.read_point_cloud(self.input_file)
        np_pcd = np.asarray(pcd.points)
        self.list_pcd = np_pcd.tolist()
    
    def write_bin(self):
        """Method to write a point cloud to a .bin file"""
        if len(self.list_intensity) == 0:
           self.list_intensity = [1 for x in range(len(self.list_pcd))]

        with open(self.output_file, "wb") as f:
            for i in range(len(self.list_pcd)):
                byte = struct.pack("ffff",*self.list_pcd[i], self.list_intensity[i])
                f.write(byte)

    def write_pcd(self):
        """Method to write a point cloud to a .pcd file"""
        np_pcd = np.asarray(self.list_pcd)
        pcd = o3d.geometry.PointCloud()
        v3d = o3d.utility.Vector3dVector
        pcd.points = v3d(np_pcd)
        o3d.io.write_point_cloud(self.output_file, pcd)

    def convert(self):
        if self.input_format == ".bin":
            self.read_bin()
            self.write_pcd()
        else:
            self.read_pcd()
            self.write_bin()
        
if __name__ == "__main__":
    input_file = r"pointcloud\input\0000000000.pcd"
    output_folder = r"pointcloud\output"
    conv = bin_pcd_converter(input_file, output_folder)
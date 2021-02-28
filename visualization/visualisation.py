class Visualization():

    from mayavi import mlab
    import numpy as np

    import visualization.visualization_data as vd
    import visualization.utils as u

    input_type = None
    input_sub_type = None
    input_name = None
    file_string = None
    BAS_filename = None
    data_source = None

    data_input = None
    molecular_system = None
    
    visualization_data = vd.VisualizationData()


    def __init__(self, input_type=None, input_sub_type=None, input_name=None, file_string=None, BAS_filename=None, data_source=None):

        if input_type is not None:
            self.input_type = input_type

        if input_sub_type is not None:
            self.input_sub_type = input_sub_type

        if input_name is not None:
            self.input_name = input_name

        if file_string is not None:
            self.file_string = file_string

        if BAS_filename is not None:
            self.BAS_filename = BAS_filename

        if data_source is not None:
            self.data_source = data_source

        if self.input_type is not None and self.input_sub_type and self.input_name is not None:
            self.initialise_data_input()

        self.initialize_molecular_system()

    def set_input_type(self, input_type):

        self.input_type = input_type

    def set_input_sub_type(self, input_sub_type):

        self.input_sub_type = input_sub_type

    def set_input_name(self, input_name):

        self.input_name = input_name

    def set_source(self, source):

        self.source = source

    def set_data_source(self, data_source):

        self.data_source = data_source

    def initialise_data_input(self):

        import visualisation.inputs

        self.data_input = visualisation.inputs.get_input(input_type='Dalton', input_sub_type='tar', input_name='tests/GVB_AB_AB_restart_1.000')


    def plot_Geometry(self, Plot_Atoms=1, Atom_Names=1, Plot_Bonds=1):

        self.mlab.figure("Geometria", bgcolor=(.5, .5, .75), size=(1000, 1000))
        self.mlab.clf()

        if Plot_Atoms:
            for i in range(self.molecular_system.nAtoms):
                self.mlab.points3d(self.molecular_system.Atoms_R[i, 0],
                                   self.molecular_system.Atoms_R[i, 1],
                                   self.molecular_system.Atoms_R[i, 2],
                                   scale_factor=self.visualization_data.Atoms_Scale[
                                       self.u.letters(self.molecular_system.Atoms_Name[i])],
                                   resolution=20,
                                   color=self.visualization_data.Atoms_Color[
                                       self.u.letters(self.molecular_system.Atoms_Name[i])],
                                   scale_mode='none')

        if Atom_Names:
            for i in range(self.molecular_system.nAtoms):
                self.mlab.text3d(self.molecular_system.Atoms_R[i, 0],
                                 self.molecular_system.Atoms_R[i, 1],
                                 self.molecular_system.Atoms_R[i, 2],
                                 self.molecular_system.Atoms_Name[i], scale=(.9, .9, .9))

        if Plot_Bonds:
            for i in range(len(self.molecular_system.Bonds)):
                self.mlab.plot3d(
                    self.np.array([self.molecular_system.Atoms_R[
                                       self.molecular_system.Atoms_Name.index(self.molecular_system.Bonds[i][0]), 0],
                                   self.molecular_system.Atoms_R[
                                       self.molecular_system.Atoms_Name.index(self.molecular_system.Bonds[i][1]), 0]]),
                    self.np.array([self.molecular_system.Atoms_R[
                                       self.molecular_system.Atoms_Name.index(self.molecular_system.Bonds[i][0]), 1],
                                   self.molecular_system.Atoms_R[
                                       self.molecular_system.Atoms_Name.index(self.molecular_system.Bonds[i][1]), 1]]),
                    self.np.array([self.molecular_system.Atoms_R[
                                       self.molecular_system.Atoms_Name.index(self.molecular_system.Bonds[i][0]), 2],
                                   self.molecular_system.Atoms_R[
                                       self.molecular_system.Atoms_Name.index(self.molecular_system.Bonds[i][1]), 2]]),
                    tube_radius=0.2, color=(233.0 / 255, 165.0 / 255, 165.0 / 255))

        self.mlab.show()

    def initialize_molecular_system(self):

        import visualisation.molecular_system

        self.molecular_system = visualisation.molecular_system.Molecular_System()

    def get_geometry(self):

        if self.data_input is None or self.molecular_system is None:

            print('Either self.data_input or self.Molecular_System')

        else:

            self.molecular_system.set_nAtoms(nAtoms=self.data_input.get_nAtoms())
            self.molecular_system.set_Atoms_R(Atoms_R=self.data_input.get_Atoms()[0])
            self.molecular_system.set_Atoms_Charge(Atoms_Charge=self.data_input.get_Atoms()[1])
            self.molecular_system.set_Atoms_Name(Atoms_Name=self.data_input.get_Atoms()[2])
            self.molecular_system.set_Bonds( Bonds=self.data_input.get_Bonds())

    def get_orbital_data(self):

        if self.data_input is None or self.molecular_system is None:

            print('Either self.data_input or self.Molecular_System')

        else:

            self.get_geometry()

            self.molecular_system.set_nb( nb=self.data_input.get_nb())
            self.molecular_system.set_Coeff(Coeff=self.data_input.get_Coeff())
            self.molecular_system.set_basis_and_norms(input=self.data_input.get_Basis())

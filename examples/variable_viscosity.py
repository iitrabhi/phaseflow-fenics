import fenics
import phaseflow

    
def variable_viscosity(m=20, start_time = 0., end_time = 1000., time_step_bounds = (0.1, 0.1, 10.),
    output_times = ('start', 1., 10., 100., 'end'), mu_s = 1.e6,
    initial_pci_refinement_cycles = 4, theta_s = 0., R_s = 0.05, restart = False):

    lid = 'near(x[1],  1.)'

    fixed_walls = 'near(x[0],  0.) | near(x[0],  1.) | near(x[1],  0.)'

    left_middle = 'near(x[0], 0.) && near(x[1], 0.5)'
    
    output_dir = 'output/variable_viscosity_m'+str(m)+'_mus'+str(mu_s)+'_thetas'+str(theta_s)+'_Rs'+str(R_s)
    
    restart_filepath=''
    
    if restart:
    
        restart_filepath = output_dir+'/restart_t'+str(start_time)+'.hdf5'
        
        output_dir = output_dir+'_restart'+str(start_time)
        
    w, mesh = phaseflow.run(
        debug = True,
        restart = restart,
        restart_filepath = restart_filepath,
        automatic_jacobian = False,
        mesh = fenics.RectangleMesh(fenics.Point(0., -0.25), fenics.Point(1., 1.), m, m, 'crossed'),
        start_time = start_time,
        end_time = end_time,
        time_step_bounds = time_step_bounds,
        output_times = output_times,
        stop_when_steady = True,
        steady_relative_tolerance = 1.e-4,
        K = 0.,
        mu_l = 0.01,
        mu_s = mu_s,
        regularization = {'a_s': 2., 'theta_s': theta_s, 'R_s': R_s},
        nlp_relative_tolerance = 1.e-4,
        nlp_max_iterations = 30,
        max_pci_refinement_cycles = 4,
        initial_pci_refinement_cycles = initial_pci_refinement_cycles,
        g = (0., 0.),
        Ste = 1.e16,
        output_dir = output_dir,
        initial_values_expression = (lid, "0.", "0.", "1. - 2.*(x[1] <= 0.)"),
        boundary_conditions = [
            {'subspace': 0, 'value_expression': ("1.", "0."), 'degree': 3, 'location_expression': lid, 'method': 'topological'},
            {'subspace': 0, 'value_expression': ("0.", "0."), 'degree': 3, 'location_expression': fixed_walls, 'method': 'topological'},
            {'subspace': 1, 'value_expression': "0.", 'degree': 2, 'location_expression': left_middle, 'method': 'pointwise'}])

            
def run_variable_viscosity():

    #variable_viscosity(theta_s = -0.01, R_s = 0.01)
    
    variable_viscosity(m = 20, mu_s = 1.e6, initial_pci_refinement_cycles = 0, theta_s = -0.01, R_s = 0.01,
        start_time = 1., end_time = 160., time_step_bounds = (1., 1., 4.),
        output_times = ('start', 10., 20., 40., 80., 'end'),
        restart = True)
    
    
if __name__=='__main__':

    run_variable_viscosity()
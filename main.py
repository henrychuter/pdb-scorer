from pyrosetta import init, pose_from_pdb, get_fa_scorefxn
init()

import tkinter as tk
from tkinter import filedialog, Button, Label


def file_upload_score():
    filepath = filedialog.askopenfilename(
            filetypes = [
                ('.pdb files', '*.pdb'),
                ('.PDB files', '*.PDB'),
                ('.pdb1 files', '*.pdb1')
            ]
        )


    if filepath:
        try:
            #regular scoring
            pose = pose_from_pdb(filepath)
            scorefxn = get_fa_scorefxn()
            total_score = scorefxn(pose)
            round_score = round(total_score, 2)

            #in depth breakdown
            pose_energies = pose.energies()
            score_types = scorefxn.get_nonzero_weighted_scoretypes()


            score_descriptions = {
                'ScoreType.fa_atr': 'Lennard-Jones attractive energy',
                'ScoreType.fa_rep': 'Lennard-Jones repulsive energy',
                'ScoreType.fa_sol': 'Lazaridis-Karplus solvation energy',
                'ScoreType.fa_intra_rep': 'Intra-residue Lennard-Jones repulsive energy',
                'ScoreType.fa_elec': 'Coulombic electrostatic energy',
                'ScoreType.pro_close': 'Proline ring closure energy & psi angle energy',
                'ScoreType.hbond_sr_bb': 'Short-range backbone-backbone hydrogen bond energy',
                'ScoreType.hbond_lr_bb': 'Long-range backbone-backbone hydrogen bond energy',
                'ScoreType.hbond_bb_sc': 'Backbone-sidechain hydrogen bond energy',
                'ScoreType.hbond_sc': 'Sidechain-sidechain hydrogen bond energy',
                'ScoreType.dslf_fa13': 'Disulfide geometry energy',
                'ScoreType.rama': 'Ramachandran energy preferences',
                'ScoreType.omega': 'Omega dihedral energy',
                'ScoreType.fa_dun': 'Internal energy of sidechain rotamers',
                'ScoreType.p_aa_pp': 'Amino acid probability energy',
                'ScoreType.yhh_planarity': 'Tyrosine hydroxyl torsion energy',
                'ScoreType.fa_intra_sol_xover4': 'Intra-residue solvation energy (4A crossover)',
                'ScoreType.lk_ball_wtd': 'Backbone geometry energy',
                'ScoreType.ref': 'Amino acid internal energy',
                'ScoreType.rama_prepro': 'Ramachandran energy preferences with proline'
            }

            protein_score = [f'{round_score} \nIn-depth breakdown:\n']

            for score_type in score_types:
                weight = scorefxn.get_weight(score_type)
                energy = pose_energies.total_energies()[score_type]
                weighted_energy = weight * energy

                display_name = score_descriptions.get(str(score_type), str(score_type))
                protein_score.append(f'{display_name}: {round(weighted_energy, 2)} (weight: {round(weight, 3)})')


            total_breakdown = '\n'.join(protein_score)
            label.config(text=f'Composite Score(negative is better): {total_breakdown}')

        except Exception as e:
            label.config(text=f'Error :( :\n{e}')
window = tk.Tk()
window.title('Protein scorer')
window.geometry('900x600')


label = Label(window, text = 'No file selected', wraplength = 750)
label.pack(pady = 10)


upload_button = Button(window, text = 'Upload file(.pdb)', command = file_upload_score)
upload_button.pack(pady = 10)


window.mainloop()
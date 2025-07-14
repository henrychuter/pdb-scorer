from pyrosetta import init, pose_from_pdb, get_fa_scorefxn
init()

import tkinter as tk
from tkinter import filedialog, Button, Label

import pymol

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

            #getting amino acid sequence
            amino_acids = pose.sequence()


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

            empty_space = []

            reg_header = f'Composite Score: {round_score}\n{"-" * 80}\nIn-Depth Breakdown\n'
            footer = f'\n{"-" * 80}'

            for score_type in score_types:
                weight = scorefxn.get_weight(score_type)
                energy = pose_energies.total_energies()[score_type]
                weighted_energy = weight * energy


                display_name = score_descriptions.get(str(score_type), str(score_type))

                empty_space.append(f'{display_name:<55}'
                                   f'{round(weighted_energy, 2):<8} (weight: {round(weight, 3)})\n')


            total_breakdown = tk.Text(window, font=('Courier New', 14), wrap = 'word', height = 36, width = 75,
                                      bg=window.cget('bg'), relief='flat', borderwidth=0)
            total_breakdown.pack(anchor = 'w', padx = 10)


            def adding_text():
                total_breakdown.delete('1.0', tk.END)
                total_breakdown.insert(tk.END, reg_header + f'\n{"".join(empty_space)}' + footer
                                       + f'\nAmino Acid Sequence\n\n{amino_acids}\n' + footer)
                total_breakdown.config(state='disabled')

                reset_button.pack(pady = 10)

                label.pack_forget()
                upload_button.pack_forget()

            adding_text()

        except Exception as e:
            label.config(text=f'Error :( :\n{e}')

def reset_fxn():
    for widget in window.winfo_children():
        widget.destroy()

    global label, upload_button, reset_button

    label = Label(window, text='No file selected', wraplength=750)
    label.pack(pady=10)

    upload_button = Button(window, text='Upload file(.pdb)', command = file_upload_score)
    upload_button.pack(pady=10)

    reset_button = Button(window, text='Reset Window', command = reset_fxn)

window = tk.Tk()
window.title('Protein scorer')
window.geometry('900x600')


label = Label(window, text = 'No file selected', wraplength = 750)
label.pack(pady = 10)

upload_button = Button(window, text = 'Upload file(.pdb)', command = file_upload_score)
upload_button.pack(pady = 10)

reset_button = Button(window, text='Reset Window', command = reset_fxn)

window.mainloop()

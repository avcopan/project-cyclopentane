# sbatch -J o2_control sim.sh o2 Z_mess_v0 . -c
# sbatch -J o2_calc sim.sh o2 Z_mess_v0 .
sbatch -J t_control sim.sh t Z_mess_v0 . -e 10 -c
sbatch -J t_calc sim.sh t Z_mess_v0 . -e 10

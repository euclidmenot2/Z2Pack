# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>
# Date:    15.10.2014 14:49:25 CEST
# File:    fp_phony.py

from common import *

import os
import re
import types
import shutil
import unittest

class BiEspressoTestCase(EspressoTestCase):
    def __init__(self, *args, **kwargs):
        self._input_folder = 'samples/espresso'

        self._input_files = [self._input_folder + '/input/' + name for name in
                             ['bi.nscf.in', 'bi.pw2wan.in', 'bi.win' ]]

        qedir = '/home/greschd/software/espresso-5.1.2/bin/'
        wandir = '/home/greschd/software/wannier90-1.2'
        mpirun = 'mpirun -np 4 '
        pwcmd = mpirun + qedir + '/pw.x '
        pw2wancmd = mpirun + qedir + '/pw2wannier90.x '
        wancmd = wandir + '/wannier90.x'
        self._z2cmd = (wancmd + ' bi -pp;' +
                       pwcmd + '< bi.nscf.in >& pw.log;' +
                       pw2wancmd + '< bi.pw2wan.in >& pw2wan.log;')

        super(BiEspressoTestCase, self).__init__(*args, **kwargs)

        self.system = z2pack.fp.System(
            self._input_files,
            [z2pack.fp.kpts.qe, z2pack.fp.kpts.wannier90],
            ['bi.nscf.in','bi.win'],
            self._z2cmd,
            executable='/bin/bash',
            mmn_path='bi.mmn',
            build_folder=self._build_folder + '/build')

    def setUp(self):
        scfdir = self._build_folder + '/scf'
        if os.path.isdir(scfdir):
            shutil.rmtree(scfdir)
        shutil.copytree(self._input_folder + '/scf', scfdir)

    def test_bismuth_0(self):
        surface = self.system.surface(lambda kx: [0, kx / 2, 0], [0, 0, 1], pickle_file=None)
        surface.wcc_calc(pos_tol=None, move_tol=None, verbose=False, num_strings=4)

        wcc = [[6.3141588123368836e-07, 0.15696321723245391, 0.15696529415637697, 0.49999732230739502, 0.49999951934079495, 0.50000090703032507, 0.50000473023724867, 0.84303590559080466, 0.84303792242658449, 0.99999970032178997], [0.043110891314299245, 0.067109240310737187, 0.26088416629439298, 0.30091006181763758, 0.46702190095374946, 0.53297834188463422, 0.69909001308067409, 0.73911609141499701, 0.9328915686473338, 0.95688886812498519], [0.046163238155185859, 0.10894340026789005, 0.24088700608583719, 0.30711836412209642, 0.43407042638237919, 0.5659279368231549, 0.69288085491668405, 0.75911157673224239, 0.89105562074174594, 0.95383637331072701], [0.042060120074521909, 0.12734787482971535, 0.22327722693870142, 0.31518186236405693, 0.41471238633256424, 0.58528840319425246, 0.68481812449980561, 0.77672480618674644, 0.87265210446769714, 0.95794097430492808], [1.6173479244672358e-05, 0.17388136651119304, 0.17390112393886878, 0.3590036931081127, 0.35902723956332339, 0.64096922155393043, 0.64099462408036567, 0.82609344277102137, 0.82611188380614353, 0.99999064806583127]]
        t_par = [0.0, 0.33333333333333331, 0.66666666666666663, 0.83333333333333326, 1.0]
        self.assertWccConv(wcc, surface.get_res()['wcc'])
        self.assertFullAlmostEqual(t_par, surface.get_res()['t_par'])

    def test_bismuth_1(self):
        surface = self.system.surface(lambda kx: [0, kx, kx], [1, 0, 0], pickle_file=None)
        surface.wcc_calc(pos_tol=None, gap_tol=None, verbose=False, num_strings=4)

        wcc = [[2.7026844783774653e-07, 0.15696295820405978, 0.15696766840373613, 0.49999835561739808, 0.49999970805503835, 0.49999998032925025, 0.5000079854154631, 0.84303572291148898, 0.84304067515945069, 0.99999968600642153], [0.0058798871053203803, 0.12754249893106184, 0.17334269139277797, 0.4322060693601264, 0.4646057527543862, 0.53539404775349997, 0.56779284268556507, 0.82665701314091722, 0.87245724758564891, 0.9941205140687166], [0.0032773470122433555, 0.13101723445411356, 0.16296228556732675, 0.38269560824843341, 0.43812987721241542, 0.56187055891363147, 0.61730480340988336, 0.83703795509553247, 0.86898339161099991, 0.99672309075785614], [0.013181953422015748, 0.12520799474151637, 0.1353770870562645, 0.3533117142464488, 0.42255114473512118, 0.57744635983435333, 0.64668699082359848, 0.86462235558571865, 0.87479079910540325, 0.98681407751024997], [0.013183253173138136, 0.12520874383562927, 0.13537738670115521, 0.35331225320504056, 0.42255261531673827, 0.57744798236665273, 0.64668774469545798, 0.86462232964677022, 0.87479135295701116, 0.98681715960456928], [0.0032772365990767337, 0.13101707151215514, 0.16296219900420267, 0.38269540347750786, 0.43812968086918463, 0.56187041641440971, 0.61730454293755577, 0.83703784459801078, 0.86898330902153509, 0.99672347511891712], [0.005878935597787625, 0.12754169151937733, 0.17334315451131846, 0.43220694570678103, 0.46460493325647279, 0.53539449505100145, 0.56779170462083095, 0.82665625341476701, 0.87245748611341112, 0.99412041520731476], [2.1848444606495693e-07, 0.15695691297115147, 0.15696932364812652, 0.49998804349669396, 0.49999968715366844, 0.50000043635922331, 0.50001512826608474, 0.84302992648503516, 0.84304170695962755, 0.99999979223793745]]
        t_par = [0.0, 0.083333333333333329, 0.16666666666666666, 0.33333333333333331, 0.66666666666666663, 0.83333333333333326, 0.91666666666666663, 1.0]
        self.assertWccConv(wcc, surface.get_res()['wcc'])
        self.assertFullAlmostEqual(t_par, surface.get_res()['t_par'])
        
    def test_bismuth_2(self):
        surface = self.system.surface(lambda kx: [0, 0, kx / 2.], [1, 1, 0], pickle_file=None)
        surface.wcc_calc(move_tol=None, gap_tol=None, verbose=False, num_strings=4)

        wcc = [[0.43459558681939453, 0.43459564506264231, 0.49999866061437553, 0.49999927418832579, 0.50000012923811554, 0.50000064779317832, 0.56540438474555765, 0.56540446863617611, 0.99999898725867331, 0.99999984249565999], [0.087508164173130037, 0.40544593893763187, 0.44154187300286174, 0.45405195146792909, 0.48412634605796206, 0.51587397648491695, 0.54594826723054568, 0.55845814536349092, 0.5945539314555095, 0.91249237633273117], [0.10900519551536474, 0.36580296453401939, 0.41655494599900644, 0.42741003368501723, 0.44472813069440098, 0.5552712870223806, 0.57259002278198201, 0.58344410783013323, 0.63419657437992827, 0.89099266196508242], [8.4321399345095059e-06, 0.38534641664707359, 0.38535414764033166, 0.42483945812195067, 0.42484121822644672, 0.57515712932558882, 0.57515901917039391, 0.61464330287362934, 0.61464920766508357, 0.99998151305432303]]
        t_par = [0.0, 0.33333333333333331, 0.66666666666666663, 1.0]
        self.assertWccConv(wcc, surface.get_res()['wcc'])
        self.assertFullAlmostEqual(t_par, surface.get_res()['t_par'])


if __name__ == "__main__":
    unittest.main()

"""
This file defines class Model.

@author: Clemens Rosenbaum :: cgbr@cs.umass.edu
@created: 6/6/18
"""
import torch
import torch.nn as nn
# from torch.multiprocessing import Pool


class Selection(nn.Module):
    """
    Class RoutingWrapperModule defines a wrapper around a regular pytorch module that computes the actual routing
    given a list of modules to choose from, and a list of actions to select a module for each sample in a batch.
    """

    def __init__(self, *modules):
        nn.Module.__init__(self)
        # self._threads = threads
        self._submodules = nn.ModuleList(modules)

    def _apply_parallel(self, arg):
        x, xm = arg
        return self._submodules[xm.next_selection](x)

    def forward(self, xs, mxs, actions):
        """
        This method takes a list of samples - a batch - and calls _forward_sample on each. Samples are
        a tensor where the first dimension is the batch dimension.
        :param samples:
        :param kwargs:
        :return:
        """
        ys = []
        xs = xs.split(split_size=1, dim=0)
        assert len(xs) == len(mxs)
        # pool = Pool(self._threads)
        # ys = pool.map(self._apply_parallel, zip(xs, mxs))
        for x, na in zip(xs, actions):
            y = self._submodules[na](x)
            ys.append(y)
        ys = torch.cat(ys, 0)
        return ys, mxs, actions

"""
A module that defines the `Path` class. See
its documentation for more information.
"""

import warnings
from tree import *
from node import *
from block import *

import garlicsim.misc.binarysearch as binarysearch

class Path(object):
    """
    A path symbolizes a line of nodes in a tree.
    A tree may be a complex tree with many junctions,
    but a path is a direct line. Therefore, a path object contains
    information about which child to choose when going through
    a node which has multiple children.
    """
    def __init__(self, tree, root=None, decisions={}):
        
        self.tree = tree

        self.root = root # The root node

        self.decisions = decisions.copy()
        """
        The decisions dict says which fork of the road the path chooses.
        It's of the form {parent_node: child_node,...}
        """


    def __len__(self):
        if self.root is None:
            return 0

        result = 0
        for j in self.iterate_blockwise():
            result += len(j)

        return result

    def __iter__(self):
        if self.root is None:
            raise StopIteration
        yield self.root
        current = self.root
        while True:
            try:
                current = self.next_node(current)
                yield current
            except IndexError:
                raise StopIteration("Ran out of tree")

    def iterate_blockwise(self, starting_at=None):
        """
        Iterates on the Path, returning Blocks when possible.
        You are allowed to specify a node/block from
        which to start iterating, using the parameter `starting_at`.
        """
        if starting_at is None:
            if self.root is None:
                raise StopIteration
            current = self.root.soft_get_block()
        else:
            current = starting_at.soft_get_block()

        yield current

        while True:
            try:
                current = self.next_node(current).soft_get_block()
                yield current
            except IndexError:
                raise StopIteration("Ran out of tree")

    def __contains__(self,thing):
        """
        Returns whether the path contains `thing`.
        `thing` may be a Node or a Block.
        """
        assert isinstance(thing,Node) or isinstance(thing,Block)

        for x in self.iterate_blockwise():
            if x is thing:
                return True
            elif isinstance(x, Block) and thing in x:
                return True
            
        return False


    def next_node(self, thing):
        """
        Returns the next node on the path.
        """
        if self.decisions.has_key(thing):
            next = self.decisions[thing]
            assert isinstance(next, Node)
            return self.decisions[thing]
        
        if isinstance(thing, Block):
            if self.decisions.has_key(thing[-1]):
                return self.decisions[thing[-1]]

        else:
            if isinstance(thing, Block):
                kids = thing[-1].children
            else:
                kids = thing.children
            if len(kids) > 0:
                kid = kids[-1]
                self.decisions[thing] = kid
                return kid

        raise IndexError("Ran out of tree")


    def __getitem__(self, i):
        """
        Gets node by number.
        """

        if isinstance(i, int):
            if i < 0:
                if i == -1:
                    return self.get_last_node()
                else: # i < -1
                    i = len(self) + i #todo: something more optimized here?

            index = -1
            for j in self.iterate_blockwise():
                index += len(j)
                if index >= i:
                    if isinstance(j,Block):
                        return j[-(index-i)-1]
                    else:
                        assert index == i
                        return j
            raise IndexError

        elif isinstance(i, slice):
            raise NotImplementedError
        else:
            return StandardError


    def get_last_node(self, starting_at=None):
        """
        Returns the last node in the path.
        Optionally, you are allowed to specify a node from
        which to start searching.
        """
        for thing in self.iterate_blockwise(starting_at=starting_at):
            pass

        if isinstance(thing, Block):
            return thing[-1]
        else:
            return thing
    
    def get_node_by_clock(self, clock, rounding="Closest"):
        my_function = lambda node: node.state.clock # Define this outside?
        return self.get_node_by_monotonic_function(function=my_function,
                                                   value=clock,
                                                   rounding=rounding)    
        
    def get_node_by_monotonic_function(self, function, value, rounding="Closest"):
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]        
        
        low = self.root
        
        if function(low) >= value:
            return binarysearch.make_both_data_into_preferred_rounding \
                   ((None, low), function, value, rounding)
        
        """
        Now we've established that the first node in the path has a lower value
        than what we're looking for.
        """
        
        for thing in self.iterate_blockwise():
            if isinstance(thing, Block):
                first = thing[0]
                if function(first) >= value:
                    return binarysearch.make_both_data_into_preferred_rounding \
                           ((low, first), function, value, rounding)
                    
                last = thing[-1]
                if function(last) >= value:
                    # It's in the block
                    return binarysearch.binary_search(thing, \
                           function, value, rounding)
                else:
                    low = last
                    continue
            else: # thing is a Node
                if function(thing) >= value:
                    return binarysearch.make_both_data_into_preferred_rounding \
                           ((low, thing), function, value, rounding)
                else:
                    low = thing
                    continue
        
        """
        If the flow reached here, that means that even the last node
        in the path has lower value than the value we're looking for.
        """
        
        return binarysearch.make_both_data_into_preferred_rounding \
               ((low, None), function, value, rounding)
            
        
    
    def get_node_occupying_timepoint(self, timepoint):
        temp = self.get_node_by_clock(timepoint, rounding="Both")
        if temp.count(None)==0:
            return temp[0]
        else:
            return None
        

    def get_existing_time_segment(self, start_time, end_time):
        """
        Between timepoints "start_time" and "end_time", returns the segment of nodes that
        exists in the Path.
        Returns the segment like so: [start,end]
        Example: In the path the first node's clock reading is 3.2, the last is 7.6.
        start_time is 2 and end_time is 5. The function will return [3.2,5]
        """

        clock_of_first = self.root.state.clock
        clock_of_last = self.get_last_node().state.clock
        
        if clock_of_first <= end_time and clock_of_last >= start_time:            
            return [max(clock_of_first, start_time),
                    min(clock_of_last, end_time)]
        else:
            return None
            


    
import networkx as net
import matplotlib.pyplot as plot
from collections import defaultdict

class MultimodeGraph(net.MultiDiGraph):
    def __init__(self,data=None,**attr):
        """Initialize a graph with edges, name, graph attributes.
        Parameters
        ----------
        data : input graph
            Data to initialize graph.  If data=None (default) an empty
            graph is created.  The data can be an edge list, or any
            NetworkX graph object.  If the corresponding optional Python
            packages are installed the data can also be a NumPy matrix
            or 2d ndarray, a SciPy sparse matrix, or a PyGraphviz graph.
        name : string, optional (default='')
            An optional name for the graph.
        attr : keyword arguments, optional (default= no attributes)
            Attributes to add to graph as key=value pairs.
        
        """
        self.parent=super(MultimodeGraph, self)
        self.nodesets=defaultdict(set)
        self.edgekeys=set()
        self.parent.__init__(data,**attr)
    
    def add_node(self, n, type=None, nodeset_id=None, attr_dict=None, **attr):
        """
        Add a node to the MultiMode graph. Behaves just like the add_node method in graph.py
        
        Parameters:
        -----------
        n: node
            A node can be any hashable Python object except None.
        type: node type
            A node type can be any hashable Python object -- but human-readable strings are preferred
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of node attributes.  Key/value pairs will
            update existing data associated with the node.
        """
        
        self.parent.add_node(n,attr_dict=attr_dict, type=type, nodeset_id=nodeset_id, **attr)
        self.nodesets[type].add(n)
    
    def add_nodes_from(self, nodes, type=None, **attr):
        """Add multiple nodes of the same type.
        
        Parameters
        ----------
        nodes : iterable container
            A container of nodes (list, dict, set, etc.).
            OR
            A container of (node, attribute dict) tuples.
            Node attributes are updated using the attribute dict.
        type: node type
            A node type can be any hashable Python object -- but human-readable strings are preferred
        attr : keyword arguments, optional (default= no attributes)
            Update attributes for all nodes in nodes.
            Node attributes specified in nodes as a tuple
            take precedence over attributes specified generally.        
        
        """
        attr['type']=type
        self.parent.add_nodes_from(nodes,**attr)
        for n in nodes: self.nodesets[type].add(n)
        
    def node_types(self):
        """ Returns a list of node types in the graph so far.
        """
        return self.nodesets.keys()
    
    def nodeset(self, type):
        """
        Returns a list of nodes of a certain type
        
        Parameters:
        -----------
        type: any hashable Python object -- but human-readable strings are preferred
        
        WILL RAISE KeyError if a type is not found -- must use try/except
        """
        return self.nodesets[type]
        
    def add_edge(self, u, v, utype=None, vtype=None, key=None, attr_dict=None, **attr):
        """Add an edge to a MultiMode / MultiPlex graph
        
        Parameters:
        -----------
        u, v: Node
            Node can be any hashable Python object except None
            
            If a node doesn't exist, it will be added to the graph
        
        utype, vtype: node type -- specify node type for nodes that must be added
            any hashable Python object -- but human-readable strings are preferred
            
            utype, vtype only must be used if the nodes don't exist in the graph already, other times are optional
            
        key: edge type
            any hashable Python object -- but human-readable strings are preferred
            
            In multi-plex graphs, multiple edge types can exist between two nodes 
            a Person-to-person graph can contain edges of type "friend", "coworker", and "relative" 
            
            key is optional if the graph is not multi-plex
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with the edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.            
        """
        
        if u not in self: self.add_node(u, type=utype)
        if v not in self: self.add_node(v, type=vtype)
        if key is not None: self.edgekeys.add((utype, vtype,key))
        self.parent.add_edge(u,v,key=key,utype=utype,vtype=vtype,attr_dict=attr_dict,**attr)
        
    def add_or_inc_edge(self,u,v,utype=None,vtype=None,key=None,attr_dict=None,**attr):
        """
        Adds an edge to the graph IF the edge does not exist already. 
        If it does exist, increment the edge weight.
        Used for quick-and-dirty calculation of projected graphs from 2-mode networks.
        """
        try:
            if self.has_edge(u,v):
                if 'weight' in self[u][v]:
                    self[u][v]['weight']+=1
                else:
                    self[u][v]['weight']=1
            else:
                self.add_edge(u,v,weight=1,utype=utype,vtype=vtype,key=key,attr_dict=attr_dict,**attr)
        except KeyError:
            self.remove_edge(u,v,key=key)
            self.add_edge(u,v,weight=1,utype=utype,vtype=vtype,key=key,attr_dict=attr_dict,**attr)
    
    def add_edges_from(self, ebunch, utype=None, vtype=None, key=None, attr_dict=None, **attr):
        """Add multiple edges of the same type to a MultiMode / MultiPlex graph
        
        Parameters:
        -----------
        ebunch : container of edges
            Each edge given in the container will be added to the
            graph. The edges must be given as as 2-tuples (u,v) or
            3-tuples (u,v,d) where d is a dictionary containing edge
            data.
        
        utype, vtype: node type -- specify node type for nodes that must be added
            any hashable Python object -- but human-readable strings are preferred
            
            utype, vtype only must be used if the nodes don't exist in the graph already, other times are optional
            
        key: edge type
            any hashable Python object -- but human-readable strings are preferred
            
            In multi-plex graphs, multiple edge types can exist between two nodes 
            a Person-to-person graph can contain edges of type "friend", "coworker", and "relative" 
            
            key is optional if the graph is not multi-plex
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with the edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.            
        """        
        
        for u,v in ebunch:
            self.add_edge(u,v,utype=utype,vtype=vtype,key=key,attr_dict=attr_dict,**attr)

    def add_weighted_edges_from(self, ebunch, utype=None, vtype=None, key=None, weight='weight', **attr):
        """Add multiple edges of the same type to a MultiMode / MultiPlex graph
        
        Parameters:
        -----------
        ebunch : container of edges
            Each edge given in the container will be added to the
            graph. The edges must be given as as 3-tuples (u,v,w) where d is a dictionary 
            containing edge data.
        
        utype, vtype: node type -- specify node type for nodes that must be added
            any hashable Python object -- but human-readable strings are preferred
            
            utype, vtype only must be used if the nodes don't exist in the graph already, other times are optional
            
        key: edge type
            any hashable Python object -- but human-readable strings are preferred
            
            In multi-plex graphs, multiple edge types can exist between two nodes 
            a Person-to-person graph can contain edges of type "friend", "coworker", and "relative" 
            
            key is optional if the graph is not multi-plex
        attr_dict : dictionary, optional (default= no attributes)
            Dictionary of edge attributes.  Key/value pairs will
            update existing data associated with the edge.
        attr : keyword arguments, optional
            Edge data (or labels or objects) can be assigned using
            keyword arguments.            
        """
        for u,v,w in ebunch:
            attr[weight]=w
            self.add_edge(u,v,utype=utype,vtype=vtype,key=key,attr_dict=attr_dict,**attr)
            
    def add_subgraph(self, graph):
        """
        Add a new subgraph to this graph. 
        
        Parameters:
        -----------
        graph:
            Multimode graph
        
        """       
        for (n, ndata) in graph.nodes_iter(data=True):
            self.add_node(n,type=ndata['type'],attr_dict=ndata)
        
        for (u,v,k,edata) in graph.edges_iter(data=True,keys=True):
            if type(edata) is not dict: continue
            self.add_edge(v,u,vtype=graph.node[u]['type'], utype=graph.node[v]['type'],key=k,attr_dict=edata)
      
         

    def subgraph(self, utype,vtype=None,key=None):
        """
        Construct a one- or a two-mode graph by extracting a subgraph from an n-mode graph
        
        Parameters
        ----------
        utype, vtype: type of nodes to extract. If vtype is not supplied, returned graph will be a 1-mode graph
        key: type of edges to extract. Get all edges between utype and vtype if key not supplied
        
        """
        if vtype is None: vtype = utype ## if only one edge type is provided, all edges are of the same type
                
        sub = MultimodeGraph()
        for f,t,k,edata in self.edges_iter(data=True, keys=True):
            if self.node[f]['type']==utype and self.node[t]['type']==vtype:
                if key is None or k==key:
                    sub.add_edge(f,t,utype=utype,vtype=vtype,key=key,attr_dict=edata)
       
        return sub
    
    def reverse(self):
        """
        Reverses the direction of edges in a directed graph. A similar function exists in NetworkX but it throws errors
        for Weighted MultiGraphs. This is a clean reimplementation.
        
        """
        out=MultimodeGraph()
        for (n, ndata) in self.nodes_iter(data=True):
            out.add_node(n,type=ndata['type'],attr_dict=ndata)
            
        for (u,v,k,edata) in self.edges_iter(data=True,keys=True):
            out.add_edge(v,u,vtype=self.node[u]['type'], utype=self.node[v]['type'],key=k,attr_dict=edata)
        return out
    
    def infer(self, subgraph1, subgraph2, key=None):
        """
        Infer a new set of edges from two 2-mode networks. This is similar to bipartite.implied_graph but uses 
        a sparse-matrix approach rather then full-matrix approach. Theoretically, the two have same computational
        complexity, but sparse-matrix approach is faster in average case, sometimes by orders of magnitude.
        
        Parameters
        ----------
        subgraph1, subgraph2:
            Multimode graphs, most likely subgraphs of a larger Multimode graph, as output by MultimodeGraph.subgraph()
        key: 
            Name of the inferred ages
        
        Example:
        --------
        colocation=mm.infer(mm.subgraph('Agent','Location'), mm.subgraph('Agent','Location').reverse(), key="colocation")
        """
        
        out=MultimodeGraph()
            
        for f,t in subgraph1.edges_iter():
            if t not in subgraph2: continue
            for t2,edata in subgraph2[t].items():
                out.add_node(f,type=subgraph1.node[f]['type'],attr_dict=subgraph1.node[f])
                out.add_node(t2,type=subgraph2.node[t2]['type'],attr_dict=subgraph2.node[t2])
                out.add_edge(f,t2,utype=subgraph1.node[f]['type'],vtype=subgraph2.node[t2]['type'],key=key)
        return out
        
    def discount_edges(self,weight_str='weight', rate=0.1):
        """
        Discount edge weights by a given rate
        
        Parameters:
        -----------
        weight_str:
            name of the parameter where edge weight is stored; defaults to "weight"
        
        rate:
            discount rate; weight(t+1)=(1-rate)*weight(t)
        
        """
        for f,t,edata in self.edges(data=True):
            if weight_str in edata:
                edata[weight_str]*=(1-rate)



    def draw(self, layout=net.spring_layout, with_labels=True):
        """
        Draw the a basic multi-colored representation of the Multimode graph. This is generally not the best representation
        of the multimode graph (as these get quite dense), but it is a definite improvement over default networkx_draw() method.
        """

        ## create a default color order and an empty color-map
        colors=['r','g','b','c','m','y','k']
        colormap={}
        d=net.degree(self)  #we use degree for sizing nodes
        pos=layout(self)  #compute layout 
        
        ## Draw each group of nodes separately, using its own color settings
        print "drawing nodes..."
        i=0
        for key in self.nodesets.keys():
            ns=[d[n]*100 for n in self.nodesets[key]]
            net.draw_networkx_nodes(self,pos,nodelist=self.nodesets[key], node_size=ns, node_color=colors[i], alpha=0.6)
            colormap[key]=colors[i]
            i+=1
            if i==len(colors): 
                i=0  ### wrap around the colormap if we run out of colors
        print colormap  
    
        ## Draw edges using a default drawing mechanism
        print "drawing edges..."
        net.draw_networkx_edges(self,pos,width=0.5,alpha=0.5)  
    
        print "drawing labels..."
        if with_labels: 
            net.draw_networkx_labels(self,pos,font_size=12)
        plot.axis('off')

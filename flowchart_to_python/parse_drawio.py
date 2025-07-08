import xml.etree.ElementTree as ET

def get_labels(mx_cells):

    edge_labels = {}

    for cell in mx_cells:
        style = cell.attrib.get("style", "")

        if "edgeLabel" in style:
            parent_edge_id = cell.attrib.get("parent","")
            label = cell.attrib.get("value", "").strip()

            if parent_edge_id and label:
                edge_labels[parent_edge_id] = label

    return edge_labels

def get_blocks_edges(mx_cells, edge_labels):

    blocks = {}
    edges = []


    for cell in mx_cells:
        id_ = cell.attrib.get("id", "")
        value = cell.attrib.get("value", "").strip()

        style = cell.attrib.get("style","")
        vertex = cell.attrib.get("vertex",  "")
        edge = cell.attrib.get("edge","")

        if vertex == "1":

            #check types
            if "ellipse" in style:
                block_type = "Start"  if "start" in value.lower() else "End" #check start or end

            elif "rhombus" in style:
                block_type =  "Decision"

            elif "rectangle" in style or "whiteSpace=wrap" in style:
                block_type = "Process"     

            else:
                # dont know type
                continue

            blocks[id_] =  {"id": id_,  "type": block_type, "text": value,"connections": []}

        elif edge == "1":
            source =cell.attrib.get("source")
            target =cell.attrib.get("target")

            label =  value or edge_labels.get(id_, None)

            if source and target:
                edges.append({"from": source, "to": target, "label": label})
    
    return blocks, edges

def parse_drawio_xml(file_path):

    tree = ET.parse(file_path)
    root = tree.getroot()

    #get cells  
    mx_cells = root.findall(".//mxCell")

    edge_label = get_labels(mx_cells) #get edge based Labels

    blocks, edges = get_blocks_edges(mx_cells, edge_label)# get blocks And Edges

    for edgepart in edges:

        if edgepart["from"] in blocks:
            
            blocks[edgepart["from"]]["connections"].append({"to":  edgepart["to"],"label":edgepart["label"] })


    return list(blocks.values())
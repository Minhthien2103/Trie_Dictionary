import os
import json
from graphviz import Digraph


class RTNode:
    def __init__(self, label = "", isEnd = False, definition = ""):
        self.label = label
        self.children = {}
        self.isEndofWord = isEnd
        self.definition = definition


class RadixTrie:
    def __init__(self):
        self.root = RTNode(isEnd = False)
    
    def get_common_prefix_length(self, str1, str2):
        i = 0

        while i < len(str1) and i < len(str2) and str1[i] == str2[i]:
            i += 1

        return i

    def insert(self, new_word, new_definition, node: RTNode = None):
        if node is None:
            node = self.root
        
        common_len = self.get_common_prefix_length(node.label, new_word)

        if common_len < (len(node.label)):
            common_prefix = node.label[:common_len]
            old_suffix = node.label[common_len:]
            new_suffix = new_word[common_len:]
            
            child_node = RTNode(label = old_suffix, isEnd = True, definition = node.definition)
            child_node.children = node.children

            node.label = common_prefix
            node.isEndofWord = False
            node.definition = ""
            node.children = {old_suffix[0]: child_node}

            if len(new_suffix) > 0:
                new_child_node = RTNode(label = new_suffix, isEnd = True, definition = new_definition)
                node.children[new_suffix[0]] = new_child_node
            
            else:
                node.isEndofWord = True
                node.definition = new_definition
        
        elif common_len == len(node.label):
            if common_len < len(new_word):
                new_suffix = new_word[common_len:]

                if new_suffix[0] in node.children:
                    self.insert(new_suffix, new_definition, node.children[new_suffix[0]])
                    
                else:
                    new_child = RTNode(new_suffix, isEnd = True, definition = new_definition)
                    node.children[new_suffix[0]] = new_child

        elif common_len == len(new_word):
            node.isEndofWord = True
            node.definition = new_definition

        
    def search(self, word, node: RTNode = None):
        if node is None:
            node = self.root

        common_len = self.get_common_prefix_length(node.label, word)

        # Không khớp hết nhãn -> Không có từ này
        if common_len < len(node.label):
            return "Không tìm thấy từ này."

        # Khớp hết nhãn
        elif common_len == len(node.label):
            # Từ cần tìm cũng vừa hết
            if common_len == len(word):
                if node.isEndofWord:
                    return node.definition
                else:
                    return "Không tìm thấy từ này."
            
            # Từ cần tìm còn dư
            elif common_len < len(word):
                new_suffix = word[common_len:]
                if new_suffix[0] in node.children:
                    return self.search(new_suffix, node.children[new_suffix[0]])
                else:
                    return "Không tìm thấy từ này."

    def delete(self, word, node: RTNode = None):
        if node is None:
            node = self.root

        common_len = self.get_common_prefix_length(node.label, word)

        if common_len < len(node.label):
            return False 
            
        elif common_len == len(node.label):
            if common_len < len(word):
                new_suffix = word[common_len:]
                if new_suffix[0] in node.children:
                    should_delete_child = self.delete(new_suffix, node.children[new_suffix[0]])
                    if should_delete_child:
                        del node.children[new_suffix[0]] 
                else:
                    return False 
                    
            elif common_len == len(word):
                if not node.isEndofWord:
                    return False 
                # Tắt trạng thái từ
                node.isEndofWord = False
                node.definition = ""

        # Nếu node không phải là từ và chỉ có 1 node con -> Gộp với con
        if not node.isEndofWord and len(node.children) == 1:
            only_child_key = list(node.children.keys())[0]
            only_child = node.children[only_child_key]
            
            # Kéo nhãn và dữ liệu của con lên cha
            node.label = node.label + only_child.label
            node.isEndofWord = only_child.isEndofWord
            node.definition = only_child.definition
            node.children = only_child.children # Trỏ tới các cháu
            
        # Báo hiệu cho node cha: "Tôi rỗng, xóa tôi đi"
        return (not node.isEndofWord) and (len(node.children) == 0)

    def save_to_json(self, filename="dictionary.json"):
        def node_to_dict(node):
            return {
                "label": node.label,
                "isEnd": node.isEndofWord,
                "def": node.definition,
                "children": {k: node_to_dict(v) for k, v in node.children.items()}
            }
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(node_to_dict(self.root), f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename="dictionary.json"):
        if not os.path.exists(filename):
            return # Nếu chưa có file thì khởi tạo cây rỗng
            
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Hàm đệ quy chuyển Dictionary ngược lại thành Node
        def dict_to_node(d):
            node = RTNode(label=d["label"], isEnd=d["isEnd"], definition=d["def"])
            node.children = {k: dict_to_node(v) for k, v in d["children"].items()}
            return node
            
        self.root = dict_to_node(data)
    
    def export_graphviz(self, filename="radix_trie_viz"):
        from graphviz import Digraph
        
        # Tạo đồ thị có hướng (Directed Graph)
        dot = Digraph(comment='Radix Trie', format='png')
        dot.attr(rankdir='TB') # Vẽ từ trên xuống (Top to Bottom)
        
        def add_nodes_edges(node):
            # Lấy địa chỉ bộ nhớ làm ID duy nhất cho node
            node_id = str(id(node))
            
            # Tùy chỉnh giao diện node
            shape = 'doublecircle' if node.isEndofWord else 'circle'
            color = 'lightblue' if node.isEndofWord else 'lightgrey'
            
            # Label hiển thị bên trong Node
            display_text = f'"{node.label}"' if node.label else '[ROOT]'
            if node.isEndofWord:
                display_text += f"\n({node.definition})"
                
            dot.node(node_id, display_text, shape=shape, style='filled', fillcolor=color, fontname="Arial")
            
            # Đệ quy vẽ các node con và mũi tên nối
            for k, child in node.children.items():
                child_id = str(id(child))
                add_nodes_edges(child)
                # Vẽ cạnh nối từ cha -> con, hiển thị ký tự đầu tiên lên cạnh
                dot.edge(node_id, child_id, label=f" {k} ", fontcolor="red", fontname="Arial")
                
        add_nodes_edges(self.root)
        
        dot.render(filename, cleanup=True) 


if __name__ == "__main__":
    trie = RadixTrie()
    
    print("--- THÊM TỪ ---")
    trie.insert("apple", "Quả táo")
    trie.insert("apply", "Nộp đơn")
    trie.insert("app", "Ứng dụng")
    print("Đã thêm: apple, apply, app")

    print("\n--- TÌM KIẾM ---")
    print("Tìm 'app':", trie.search("app"))
    print("Tìm 'apple':", trie.search("apple"))
    print("Tìm 'apply':", trie.search("apply"))
    print("Tìm 'application':", trie.search("application"))

    print("\n--- XÓA ---")
    print("Xóa 'apple'...")
    trie.delete("apple")
    print("Tìm lại 'apple':", trie.search("apple"))
    print("Tìm 'apply' (vẫn phải còn):", trie.search("apply"))
use grapl_graph_descriptions::graph_description::*;
use grapl_graph_descriptions::graph_description::{Static, IdStrategy};

use derive_dynamic_node::{DynamicNode as GraplNode};

#[derive(Clone, GraplNode)]
pub struct Auid {
    auid: u64,
}

pub fn static_strategy() -> IdStrategy {
    Static {
        primary_key_properties: vec![
            "auid".to_string()
        ],
        primary_key_requires_asset_id: true,
    }.into()
}

impl IAuidNode for AuidNode {
    fn get_mut_dynamic_node(&mut self) -> &mut DynamicNode {
        &mut self.dynamic_node
    }
}




#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}

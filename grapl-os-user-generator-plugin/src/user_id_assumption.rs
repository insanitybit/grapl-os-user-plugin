use grapl_graph_descriptions::graph_description::*;
use grapl_graph_descriptions::graph_description::{Static, IdStrategy};

use derive_dynamic_node::{DynamicNode as GraplNode};

pub const ASSUMED_USER_ID: &'static str = "assumed_user_id";
pub const ASSUMING_PROCESS: &'static str = "assuming_process";

#[derive(Clone, GraplNode)]
pub struct UserIdAssumption {
    user_id: u64,
    assuming_process_id: u64,
    assumed_timestamp: u64,
}

pub fn static_strategy() -> IdStrategy {
    Static {
        primary_key_properties: vec![
            "user_id".to_string(),
            "assuming_process_id".to_string(),
            "assumed_timestamp".to_string(),
        ],
        primary_key_requires_asset_id: true,
    }.into()
}

impl IUserIdAssumptionNode for UserIdAssumptionNode {
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

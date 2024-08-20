from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class EigenbotRoughCfg( LeggedRobotCfg ):
    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.42] # x,y,z [m]
        default_joint_angles = { # = target angles [rad] when action = 0.0
            'bendy_joint_M1_S1': 0.1,   # [rad]
            'bendy_joint_M2_S2': 0.1,   # [rad]
            'bendy_joint_M3_S3': 0.1,
            'bendy_joint_M4_S4': 0.1,
            'bendy_joint_M5_S5': 0.1,
            'bendy_joint_M6_S6': 0.1,
            'bendy_joint_M7_S7': 0.1,
            'bendy_joint_M8_S8': 0.1,
            'bendy_joint_M9_S9': 0.1,
            'bendy_joint_M10_S10': 0.1,
            'bendy_joint_M11_S11': 0.1,
            'bendy_joint_M12_S12': 0.1,
            'bendy_joint_M13_S13': 0.1,
            'bendy_joint_M14_S14': 0.1,
            'bendy_joint_M15_S15': 0.1,
            'bendy_joint_M16_S16': 0.1,
            'bendy_joint_M17_S17': 0.1,
            'bendy_joint_M18_S18': 0.1,
            
            }

    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 20}  # [N*m/rad]
        damping = {'joint': 0.5}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4

    class asset( LeggedRobotCfg.asset ):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/eigenbot/urdf/eigenbot_hexapod.urdf'
        name = "eigenbot"
        foot_name = "foot"
        penalize_contacts_on = ["thigh", "calf"]
        terminate_after_contacts_on = ["base"]
        self_collisions = 1 # 1 to disable, 0 to enable...bitwise filter
  
    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.25
        class scales( LeggedRobotCfg.rewards.scales ):
            torques = -0.0002
            dof_pos_limits = -10.0
    class env(LeggedRobotCfg.env):
        num_actions=18

class EigenbotRoughCfgPPO( LeggedRobotCfgPPO ):
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01

import express from "express";
import { authenticate } from "../middleware/auth.middleware";
import { authorize } from "../middleware/role.middleware";

const router = express.Router();

router.get(
  "/profile",
  authenticate,
  (req, res) => {
    res.json({
      user: req.user
    });
  }
);

router.get(
  "/admin",
  authenticate,
  authorize("admin"),
  (req, res) => {
    res.json({
      message: "Admin Access Granted"
    });
  }
);

router.get(
  "/user",
  authenticate,
  authorize("admin", "user"),
  (req, res) => {
    res.json({
      message: "User Access Granted"
    });
  }
);

export default router;
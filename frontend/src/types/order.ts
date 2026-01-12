import { BaseRecord } from "@refinedev/core";

export interface IOrder extends BaseRecord {
  id: number;
  adresse: string;
  type: string;
  ordre_passage: number;
}
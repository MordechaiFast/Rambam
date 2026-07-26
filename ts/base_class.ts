/**
 * Base class for a compound unit, made up of subunits.
 *
 * The names of the units and subunits, and the number of subunits in each
 * unit or next greater subunit must be given in a dict that is a class
 * variable.
 * This must be assigned with the first object of the class type.
 * After this has been assigned, it cannot be changed.
 */
export abstract class MeasureWithSubunits {
  /** The names of the units and subunits, and the number of subunits that make up each unit */
  static units: Record<string, number> = {};

  /** Whether to constrict the basic unit in a repeating cycle or not */
  static cycle: boolean = false;

  /** Used for division. Must be assigned after the child class has been defined */
  static child_class: typeof MeasureWithSubunits | null = null;

  /** If true, equality/comparison with other types returns false or raises TypeError */
  static strict: boolean = true;

  protected unit_list: string[];
  protected unit_values: Record<string, number> = {};

  /**
   * Create a new MeasureWithSubunits instance
   * @param args - The measure values in unit order
   * @param units - Optional unit mapping (only used on first instantiation)
   */
  constructor(...args: number[]) {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;

    // Ensure units are defined
    if (UnitsClass.units && Object.keys(UnitsClass.units).length === 0) {
      throw new Error('Must supply unit mapping');
    }

    this.unit_list = Object.keys(UnitsClass.units);
    const subunits = Object.values(UnitsClass.units);

    // Initialize measures array
    const measures: number[] = this.unit_list.map((_, i) =>
      i < args.length ? args[i] : 0
    );

    // Reduce: handle fractional parts and carry from least significant
    let carry = 0;
    for (let i = 0; i < this.unit_list.length; i++) {
      measures[i] += carry * subunits[i];
      const [whole, frac] = this.divmod(measures[i], 1);
      measures[i] = whole;
      carry = frac;
    }

    // Carry from most significant back
    carry = 0;
    for (let i = this.unit_list.length - 1; i >= 0; i--) {
      measures[i] += carry;
      const [frac, whole] = this.divmod(measures[i], subunits[i]);
      carry = frac;
      measures[i] = whole;
    }

    measures[0] += carry;

    // Apply cycle constraint if needed
    if (UnitsClass.cycle && measures[0] !== 0) {
      measures[0] = ((measures[0] % subunits[0]) + subunits[0]) % subunits[0];
    }

    // Assign values
    for (let i = 0; i < this.unit_list.length; i++) {
      this.unit_values[this.unit_list[i]] = Math.floor(measures[i]);
    }
  }

  /** Helper: divmod implementation (dividend, divisor) -> [quotient, remainder] */
  private divmod(a: number, b: number): [number, number] {
    return [Math.floor(a / b), a % b];
  }

  /** Get a unit value by index or name */
  get(index: number | string): number {
    if (typeof index === 'number') {
      return this.unit_values[this.unit_list[index]];
    }
    return this.unit_values[index] ?? 0;
  }

  /** Get units by slice notation */
  slice(start?: number, end?: number): number[] {
    const s = start ?? 0;
    const e = end ?? this.unit_list.length;
    return this.unit_list
      .slice(s, e)
      .map(unit => this.unit_values[unit]);
  }

  /** Get all unit values as an array */
  toArray(): number[] {
    return this.unit_list.map(unit => this.unit_values[unit]);
  }

  /** Length (number of units) */
  get length(): number {
    return this.unit_list.length;
  }

  /** String representation */
  toString(): string {
    return '(' + this.toArray().join(', ') + ')';
  }

  /** Debug representation */
  [Symbol.for('nodejs.util.inspect.custom')](): string {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    const measures = this.toArray().join(', ');
    return `${UnitsClass.name}(${measures}, units=${JSON.stringify(UnitsClass.units)})`;
  }

  /** Hash code for use in sets/maps */
  hashCode(): number {
    let hash = 0;
    for (const val of this.toArray()) {
      hash = ((hash << 5) - hash) + val;
      hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
  }

  // ==================== Comparison Operators ====================

  equals(other: MeasureWithSubunits | any): boolean {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    if (UnitsClass.strict && !(other instanceof UnitsClass)) {
      return false;
    }

    const thisArr = this.toArray();
    const otherArr = other instanceof MeasureWithSubunits ? other.toArray() : [];

    const maxLen = Math.max(thisArr.length, otherArr.length);
    for (let i = 0; i < maxLen; i++) {
      const a = thisArr[i] ?? 0;
      const b = otherArr[i] ?? 0;
      if (a !== b) return false;
    }
    return true;
  }

  greaterThan(other: MeasureWithSubunits): boolean {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    if (UnitsClass.strict && !(other instanceof UnitsClass)) {
      throw new TypeError(
        `'>' not supported between instances of '${UnitsClass.name}' and '${other.constructor.name}'`
      );
    }

    const thisArr = this.toArray();
    const otherArr = other.toArray();
    const maxLen = Math.max(thisArr.length, otherArr.length);

    for (let i = 0; i < maxLen; i++) {
      const a = thisArr[i] ?? 0;
      const b = otherArr[i] ?? 0;
      if (a > b) return true;
      if (a < b) return false;
    }
    return false;
  }

  lessThan(other: MeasureWithSubunits): boolean {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    if (UnitsClass.strict && !(other instanceof UnitsClass)) {
      throw new TypeError(
        `'<' not supported between instances of '${UnitsClass.name}' and '${other.constructor.name}'`
      );
    }

    const thisArr = this.toArray();
    const otherArr = other.toArray();
    const maxLen = Math.max(thisArr.length, otherArr.length);

    for (let i = 0; i < maxLen; i++) {
      const a = thisArr[i] ?? 0;
      const b = otherArr[i] ?? 0;
      if (a < b) return true;
      if (a > b) return false;
    }
    return false;
  }

  greaterThanOrEqual(other: MeasureWithSubunits): boolean {
    return this.greaterThan(other) || this.equals(other);
  }

  lessThanOrEqual(other: MeasureWithSubunits): boolean {
    return this.lessThan(other) || this.equals(other);
  }

  // ==================== Math Operators ====================

  add(addend: MeasureWithSubunits): MeasureWithSubunits {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    if (UnitsClass.strict && !(addend instanceof UnitsClass)) {
      throw new TypeError(
        `'+' not supported between instances of '${UnitsClass.name}' and '${addend.constructor.name}'`
      );
    }

    const thisArr = this.toArray();
    const otherArr = addend.toArray();
    const maxLen = Math.max(thisArr.length, otherArr.length);
    const result: number[] = [];

    for (let i = 0; i < maxLen; i++) {
      result.push((thisArr[i] ?? 0) + (otherArr[i] ?? 0));
    }

    return new UnitsClass(...result);
  }

  subtract(subtrahend: MeasureWithSubunits): MeasureWithSubunits {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    if (UnitsClass.strict && !(subtrahend instanceof UnitsClass)) {
      throw new TypeError(
        `'-' not supported between instances of '${UnitsClass.name}' and '${subtrahend.constructor.name}'`
      );
    }

    const thisArr = this.toArray();
    const otherArr = subtrahend.toArray();
    const maxLen = Math.max(thisArr.length, otherArr.length);
    const result: number[] = [];

    for (let i = 0; i < maxLen; i++) {
      result.push((thisArr[i] ?? 0) - (otherArr[i] ?? 0));
    }

    return new UnitsClass(...result);
  }

  multiply(factor: number): MeasureWithSubunits {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    const result = this.toArray().map(x => x * factor);
    return new UnitsClass(...result);
  }

  divide(divisor: number | MeasureWithSubunits): number | MeasureWithSubunits {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;

    if (divisor instanceof MeasureWithSubunits) {
      // Ratio calculation
      const thisArr = this.toArray();
      const otherArr = divisor.toArray();
      const subunits = Object.values(UnitsClass.units);

      let numerator = 0;
      let denominator = 0;

      const maxLen = Math.max(thisArr.length, otherArr.length);
      for (let i = 0; i < maxLen; i++) {
        const a = thisArr[i] ?? 0;
        const b = otherArr[i] ?? 0;
        numerator = numerator * (subunits[i] ?? 1) + a;
        denominator = denominator * (subunits[i] ?? 1) + b;
      }

      return denominator !== 0 ? numerator / denominator : 0;
    } else {
      // Scalar division
      if (UnitsClass.child_class) {
        const result = this.toArray().map(x => x / divisor);
        return new UnitsClass.child_class(...result, 0);
      } else {
        throw new TypeError(
          `Division is not supported for type '${typeof divisor}'`
        );
      }
    }
  }

  negate(): MeasureWithSubunits {
    return this.multiply(-1);
  }

  absolute(): MeasureWithSubunits {
    const zeroInstance = new (this.constructor as typeof MeasureWithSubunits)();
    if (this.lessThan(zeroInstance)) {
      return this.negate();
    }
    return this;
  }

  round(): number {
    const UnitsClass = this.constructor as typeof MeasureWithSubunits;
    const subunits = Object.values(UnitsClass.units);
    const secondVal = this.get(1);

    if (secondVal < (subunits[1] ?? 1) / 2) {
      return this.get(0);
    } else {
      return this.get(0) + 1;
    }
  }
}
